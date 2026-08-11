"""Deterministic provider used by the credential-free execution path."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from time import perf_counter

from ..token_usage import estimate_tokens
from .base import GenerationRequest, ModelResponse, StructuredModelResponse, Usage


FixtureResponder = Callable[[GenerationRequest], str]


def _default_response(request: GenerationRequest) -> str:
    digest = hashlib.sha256(
        f"{request.instructions}\n{request.input}".encode("utf-8")
    ).hexdigest()[:12]
    return f"offline-fixture:{digest}"


class DeterministicProvider:
    """Run a lab-defined fixture through the same contract as a live model."""

    name = "mock"

    def __init__(self, responder: FixtureResponder | None = None) -> None:
        self._responder = responder or _default_response

    @property
    def available(self) -> bool:
        return True

    def generate(self, request: GenerationRequest) -> ModelResponse:
        started = perf_counter()
        text = self._responder(request)
        elapsed = perf_counter() - started
        input_tokens = estimate_tokens(f"{request.instructions}\n{request.input}")
        output_tokens = estimate_tokens(text)
        return ModelResponse(
            text=text,
            provider=self.name,
            model=request.model or "deterministic-fixture-v1",
            elapsed_seconds=elapsed,
            usage=Usage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                source="estimated",
            ),
            mode="offline",
            metadata={"measurement": "local wall clock", "deterministic": True},
        )

    def generate_structured(self, request: GenerationRequest, response_model):
        """Validate a fixture response with the same Pydantic type used live."""

        response = self.generate(request)
        return StructuredModelResponse(
            value=response_model.model_validate_json(response.text),
            response=response,
        )
