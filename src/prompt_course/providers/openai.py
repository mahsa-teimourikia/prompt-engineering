"""Optional OpenAI Responses API adapter.

The SDK and API key are deliberately loaded only when this provider is used.
"""

from __future__ import annotations

import importlib.util
import os
from time import perf_counter
from typing import Any

from .base import (
    GenerationRequest,
    ModelResponse,
    ProviderUnavailableError,
    StructuredModelResponse,
    Usage,
)


def _usage_value(usage: Any, name: str) -> int | None:
    value = getattr(usage, name, None)
    return int(value) if value is not None else None


class OpenAIProvider:
    name = "openai"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.6")

    @property
    def available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY")) and importlib.util.find_spec("openai") is not None

    def generate(self, request: GenerationRequest) -> ModelResponse:
        if not self.available:
            raise ProviderUnavailableError(
                "OpenAI live mode requires the openai package and OPENAI_API_KEY. "
                "See the root README; never paste a key into a notebook."
            )

        from openai import OpenAI

        client = OpenAI()
        model = request.model or self.model
        started = perf_counter()
        response = client.responses.create(
            model=model,
            instructions=request.instructions or None,
            input=request.input,
            max_output_tokens=request.max_output_tokens,
            store=False,
        )
        elapsed = perf_counter() - started
        usage = getattr(response, "usage", None)
        input_tokens = _usage_value(usage, "input_tokens")
        output_tokens = _usage_value(usage, "output_tokens")
        total_tokens = _usage_value(usage, "total_tokens")
        if total_tokens is None and input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens

        return ModelResponse(
            text=response.output_text,
            provider=self.name,
            model=model,
            elapsed_seconds=elapsed,
            usage=Usage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                source="provider" if usage is not None else "unavailable",
            ),
            mode="live",
            response_id=getattr(response, "id", None),
            metadata={"measurement": "client wall clock", "stored": False},
        )

    def generate_structured(self, request: GenerationRequest, response_model):
        """Use the Responses API Pydantic parser, then retain usage and timing."""

        if not self.available:
            raise ProviderUnavailableError(
                "OpenAI live mode requires the openai package and OPENAI_API_KEY. "
                "See the root README; never paste a key into a notebook."
            )

        from openai import OpenAI

        client = OpenAI()
        model = request.model or self.model
        started = perf_counter()
        response = client.responses.parse(
            model=model,
            input=[
                {"role": "developer", "content": request.instructions},
                {"role": "user", "content": request.input},
            ],
            text_format=response_model,
            max_output_tokens=request.max_output_tokens,
            store=False,
        )
        elapsed = perf_counter() - started
        if response.output_parsed is None:
            raise ValueError("provider returned no parsed value; inspect refusal/output metadata")
        usage = getattr(response, "usage", None)
        input_tokens = _usage_value(usage, "input_tokens")
        output_tokens = _usage_value(usage, "output_tokens")
        total_tokens = _usage_value(usage, "total_tokens")
        if total_tokens is None and input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens
        observed = ModelResponse(
            text=response.output_text,
            provider=self.name,
            model=model,
            elapsed_seconds=elapsed,
            usage=Usage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                source="provider" if usage is not None else "unavailable",
            ),
            mode="live",
            response_id=getattr(response, "id", None),
            metadata={"measurement": "client wall clock", "stored": False, "structured": True},
        )
        return StructuredModelResponse(value=response.output_parsed, response=observed)
