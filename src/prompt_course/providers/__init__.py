"""Model-provider contracts and adapters.

The deterministic adapter is always available. Optional live adapters load
their SDKs lazily so repository tests never require credentials or network
access.
"""

from .base import (
    GenerationRequest,
    ModelProvider,
    ModelResponse,
    ProviderUnavailableError,
    StructuredModelResponse,
    Usage,
)
from .factory import get_provider
from .mock import DeterministicProvider
from .openai import OpenAIProvider

__all__ = [
    "DeterministicProvider",
    "GenerationRequest",
    "ModelProvider",
    "ModelResponse",
    "OpenAIProvider",
    "ProviderUnavailableError",
    "StructuredModelResponse",
    "Usage",
    "get_provider",
]
