"""Provider-neutral model requests with deterministic replay support."""

from __future__ import annotations

import hashlib
import json
import math
import mimetypes
import os
import warnings
from pathlib import Path
from typing import Any, Literal, Protocol

from pydantic import BaseModel, Field, ConfigDict


DEFAULT_MODEL = os.environ.get("NORTHSTAR_MODEL", "gemini-2.5-flash")
HASH_EMBEDDING_NOTICE = (
    "Hash embeddings are not semantic; they are suitable only for making "
    "retrieval code paths run in offline demonstrations."
)


class ConfigError(RuntimeError):
    """Raised when the requested runtime mode is not configured."""


class MissingReplayError(LookupError):
    """Raised when a replay request has no recorded response."""

    def __init__(self, case_id: str, fingerprint: str) -> None:
        self.case_id = case_id
        self.fingerprint = fingerprint
        super().__init__(
            f"No replay exists for case_id={case_id!r} "
            f"(fingerprint={fingerprint}). Set NORTHSTAR_MODE=record to "
            "record a response."
        )


class Part(BaseModel):
    """One typed part of a message."""

    kind: Literal["text", "image", "tool_result"]
    text: str | None = None
    path: str | None = None
    tool_name: str | None = None
    payload: dict[str, Any] | None = None


class Message(BaseModel):
    """A message sent to or returned by a model."""

    role: Literal["user", "model", "tool"]
    text: str = ""
    parts: list[Part] = Field(default_factory=list)


class ToolSpec(BaseModel):
    """A JSON-schema declaration for a callable application tool."""

    name: str
    description: str
    parameters: dict[str, Any]


class PromptRequest(BaseModel):
    """A stable, fingerprintable model request."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    case_id: str
    system: str | None = None
    messages: list[Message]
    response_schema: type[BaseModel] | None = Field(
        default=None,
        exclude=True,
    )
    tools: list[ToolSpec] = Field(default_factory=list)
    temperature: float = 0.0
    model: str = Field(default_factory=lambda: os.environ.get("NORTHSTAR_MODEL", DEFAULT_MODEL))

    @property
    def schema_name(self) -> str | None:
        return self.response_schema.__name__ if self.response_schema else None

    def fingerprint(self) -> str:
        """Return a stable SHA-256 fingerprint, deliberately excluding model."""

        schema = (
            self.response_schema.model_json_schema()
            if self.response_schema is not None
            else None
        )
        payload = {
            "system": self.system,
            "messages": [
                {
                    "role": message.role,
                    "text": message.text,
                    "parts": [
                        {
                            "kind": part.kind,
                            "text": part.text,
                            "path": part.path,
                            "tool_name": part.tool_name,
                            "payload": part.payload,
                        }
                        for part in message.parts
                    ],
                }
                for message in self.messages
            ],
            "schema_name": self.schema_name,
            "schema": schema,
            "tools": [tool.name for tool in self.tools],
            "temperature": self.temperature,
        }
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class ToolCall(BaseModel):
    """A function call proposed by a model."""

    name: str
    arguments: dict[str, Any]


class Usage(BaseModel):
    """Token usage, marked when it is an offline estimate."""

    input_tokens: int
    output_tokens: int
    estimated: bool


class ModelResponse(BaseModel):
    """Normalized response from either replay or live execution."""

    case_id: str
    text: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    parsed: Any | None = None
    parse_error: str | None = None
    usage: Usage
    source: Literal["replay", "live"]
    fingerprint: str
    stale: bool = False


class ModelClient(Protocol):
    """Common interface implemented by replay and provider clients."""

    def generate(self, request: PromptRequest) -> ModelResponse:
        ...

    def embed(self, texts: list[str], *, case_id: str) -> list[list[float]]:
        ...


def estimate_tokens(text: str) -> int:
    """Estimate tokens roughly for cost reasoning; this is not a tokenizer."""

    return max(1, math.ceil(len(text) / 4))


def _strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].strip().lower() in {"```", "```json"}:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return stripped


def _parse_response(schema: type[BaseModel] | None, text: str) -> tuple[Any | None, str | None]:
    if schema is None:
        return None, None
    try:
        return schema.model_validate_json(_strip_json_fence(text)), None
    except Exception as exc:
        return None, str(exc)


def _request_text(request: PromptRequest) -> str:
    return " ".join(
        [request.system or ""]
        + [message.text for message in request.messages]
        + [
            part.text or ""
            for message in request.messages
            for part in message.parts
        ]
    )


def _hash_embedding(text: str) -> list[float]:
    vector = [0.0] * 64
    for token in text.split():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        vector[int.from_bytes(digest[:2], "big") % 64] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


class ReplayClient:
    """Serve recorded model responses and deterministic hash embeddings."""

    def __init__(self, replay_path: Path) -> None:
        self.replay_path = Path(replay_path)
        self.records = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self.replay_path.exists():
            return {}
        return json.loads(self.replay_path.read_text(encoding="utf-8"))

    def generate(self, request: PromptRequest) -> ModelResponse:
        fingerprint = request.fingerprint()
        try:
            record = self.records[request.case_id]
        except KeyError as exc:
            raise MissingReplayError(request.case_id, fingerprint) from exc

        recorded_fingerprint = record["fingerprint"]
        stale = recorded_fingerprint != fingerprint
        if stale:
            warnings.warn(
                f"Replay fingerprint mismatch for case_id={request.case_id!r}: "
                f"recorded {recorded_fingerprint}, requested {fingerprint}",
                RuntimeWarning,
                stacklevel=2,
            )
        text = str(record.get("text", ""))
        usage_data = record.get("usage")
        if usage_data is None:
            usage = Usage(
                input_tokens=estimate_tokens(_request_text(request)),
                output_tokens=estimate_tokens(text),
                estimated=True,
            )
        else:
            usage = Usage.model_validate(usage_data)
        parsed, parse_error = _parse_response(request.response_schema, text)
        return ModelResponse(
            case_id=request.case_id,
            text=text,
            tool_calls=[ToolCall.model_validate(item) for item in record.get("tool_calls", [])],
            parsed=parsed,
            parse_error=parse_error,
            usage=usage,
            source="replay",
            fingerprint=recorded_fingerprint,
            stale=stale,
        )

    def embed(self, texts: list[str], *, case_id: str) -> list[list[float]]:
        """Return non-semantic hash vectors so retrieval paths run offline."""

        return [_hash_embedding(text) for text in texts]


class GeminiClient:
    """Thin adapter around the lazily imported google-genai SDK."""

    def __init__(self) -> None:
        from google import genai

        self._genai = genai
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def _contents(self, request: PromptRequest, types: Any) -> list[Any]:
        contents = []
        for message in request.messages:
            parts = []
            if message.text:
                parts.append(types.Part.from_text(text=message.text))
            for item in message.parts:
                if item.kind == "text":
                    parts.append(types.Part.from_text(text=item.text or ""))
                elif item.kind == "image":
                    if not item.path:
                        raise ValueError("image parts require path")
                    path = Path(item.path)
                    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                    parts.append(types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type))
                else:
                    parts.append(
                        types.Part.from_text(
                            text=json.dumps(
                                {
                                    "tool_name": item.tool_name,
                                    "payload": item.payload,
                                },
                                sort_keys=True,
                            )
                        )
                    )
            contents.append(
                types.Content(
                    role="model" if message.role == "model" else "user",
                    parts=parts,
                )
            )
        return contents

    def generate(self, request: PromptRequest) -> ModelResponse:
        from google.genai import types

        declarations = [
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters_json_schema=tool.parameters,
            )
            for tool in request.tools
        ]
        config_kwargs: dict[str, Any] = {
            "system_instruction": request.system,
            "temperature": request.temperature,
        }
        if request.response_schema is not None:
            config_kwargs.update(
                response_mime_type="application/json",
                response_schema=request.response_schema,
            )
        if declarations:
            config_kwargs["tools"] = [types.Tool(function_declarations=declarations)]
        response = self._client.models.generate_content(
            model=request.model,
            contents=self._contents(request, types),
            config=types.GenerateContentConfig(**config_kwargs),
        )
        text = response.text or ""
        calls = [
            ToolCall(name=call.name or "", arguments=call.args or {})
            for call in (response.function_calls or [])
        ]
        parsed = response.parsed
        parse_error = None
        if request.response_schema is not None and parsed is None:
            parsed, parse_error = _parse_response(request.response_schema, text)
        usage_metadata = response.usage_metadata
        usage = Usage(
            input_tokens=usage_metadata.prompt_token_count if usage_metadata and usage_metadata.prompt_token_count is not None else estimate_tokens(_request_text(request)),
            output_tokens=usage_metadata.candidates_token_count if usage_metadata and usage_metadata.candidates_token_count is not None else estimate_tokens(text),
            estimated=usage_metadata is None
            or usage_metadata.prompt_token_count is None
            or usage_metadata.candidates_token_count is None,
        )
        return ModelResponse(
            case_id=request.case_id,
            text=text,
            tool_calls=calls,
            parsed=parsed,
            parse_error=parse_error,
            usage=usage,
            source="live",
            fingerprint=request.fingerprint(),
            stale=False,
        )

    def embed(self, texts: list[str], *, case_id: str) -> list[list[float]]:
        from google.genai import types

        del case_id
        response = self._client.models.embed_content(
            model=os.environ.get("NORTHSTAR_EMBED_MODEL", "gemini-embedding-001"),
            contents=texts,
            config=types.EmbedContentConfig(output_dimensionality=64),
        )
        return [embedding.values or [] for embedding in response.embeddings or []]


class RecordingClient:
    """Wrap a live client and persist replay records after each generation."""

    def __init__(self, inner: ModelClient, replay_path: Path) -> None:
        self.inner = inner
        self.replay_path = Path(replay_path)
        self.records = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self.replay_path.exists():
            return {}
        return json.loads(self.replay_path.read_text(encoding="utf-8"))

    def generate(self, request: PromptRequest) -> ModelResponse:
        response = self.inner.generate(request)
        self.records[request.case_id] = {
            "fingerprint": request.fingerprint(),
            "text": response.text,
            "tool_calls": [call.model_dump(mode="json") for call in response.tool_calls],
            "usage": response.usage.model_dump(mode="json"),
            "recorded_model": request.model,
        }
        self.replay_path.parent.mkdir(parents=True, exist_ok=True)
        self.replay_path.write_text(
            json.dumps(self.records, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return response

    def embed(self, texts: list[str], *, case_id: str) -> list[list[float]]:
        return self.inner.embed(texts, case_id=case_id)


def get_client(replay_path: Path) -> ModelClient:
    """Build the client selected by NORTHSTAR_MODE and print its banner."""

    mode = os.environ.get("NORTHSTAR_MODE", "replay").lower()
    replay_path = Path(replay_path)
    if mode == "replay":
        print("northstar mode: REPLAY — responses are recorded fixtures, not live model output")
        return ReplayClient(replay_path)
    if mode not in {"live", "record"}:
        raise ConfigError("NORTHSTAR_MODE must be one of replay, live, or record")
    if not os.environ.get("GEMINI_API_KEY"):
        raise ConfigError(f"{mode} mode requires GEMINI_API_KEY")
    inner = GeminiClient()
    if mode == "live":
        print(
            "northstar mode: LIVE — calling "
            f"{os.environ.get('NORTHSTAR_MODEL', DEFAULT_MODEL)}"
        )
        return inner
    print(
        f"northstar mode: RECORD — calling "
        f"{os.environ.get('NORTHSTAR_MODEL', DEFAULT_MODEL)} and writing {replay_path}"
    )
    return RecordingClient(inner, replay_path)
