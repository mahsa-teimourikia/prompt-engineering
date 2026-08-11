"""Portable contracts shared by offline and live model providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Literal, Mapping, Protocol, TypeVar, runtime_checkable


UsageSource = Literal["provider", "estimated", "unavailable"]
ExecutionMode = Literal["offline", "live"]
StructuredValue = TypeVar("StructuredValue")


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """One provider-neutral text-generation request.

    Business policy belongs in the application or lab, while `instructions`
    contains the behavioral contract sent to the selected model adapter.
    """

    input: str
    instructions: str = ""
    model: str | None = None
    max_output_tokens: int = 800
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.input.strip():
            raise ValueError("GenerationRequest.input must not be empty")
        if self.max_output_tokens < 1:
            raise ValueError("max_output_tokens must be positive")


@dataclass(frozen=True, slots=True)
class Usage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    source: UsageSource = "unavailable"

    def __post_init__(self) -> None:
        values = (self.input_tokens, self.output_tokens, self.total_tokens)
        if any(value is not None and value < 0 for value in values):
            raise ValueError("token counts cannot be negative")


@dataclass(frozen=True, slots=True)
class ModelResponse:
    text: str
    provider: str
    model: str
    elapsed_seconds: float
    usage: Usage
    mode: ExecutionMode
    response_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.elapsed_seconds < 0:
            raise ValueError("elapsed_seconds cannot be negative")


@dataclass(frozen=True, slots=True)
class StructuredModelResponse(Generic[StructuredValue]):
    """A validated value paired with its observable provider response."""

    value: StructuredValue
    response: ModelResponse


class ProviderUnavailableError(RuntimeError):
    """Raised when a requested live provider is not configured."""


@runtime_checkable
class ModelProvider(Protocol):
    name: str

    @property
    def available(self) -> bool: ...

    def generate(self, request: GenerationRequest) -> ModelResponse: ...
