"""Shared, provider-neutral infrastructure for the practical course labs."""

from .datasets import Case, deterministic_split, load_jsonl, slice_counts
from .evaluation import (
    EvaluationRecord,
    EvaluationSummary,
    bootstrap_interval,
    evaluate_cases,
)
from .providers import (
    DeterministicProvider,
    GenerationRequest,
    ModelResponse,
    OpenAIProvider,
    ProviderUnavailableError,
    StructuredModelResponse,
    Usage,
    get_provider,
)

__all__ = [
    "Case",
    "DeterministicProvider",
    "EvaluationRecord",
    "EvaluationSummary",
    "GenerationRequest",
    "ModelResponse",
    "OpenAIProvider",
    "ProviderUnavailableError",
    "StructuredModelResponse",
    "Usage",
    "bootstrap_interval",
    "deterministic_split",
    "evaluate_cases",
    "get_provider",
    "load_jsonl",
    "slice_counts",
]
