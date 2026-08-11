"""Provider selection controlled explicitly by environment or notebook code."""

from __future__ import annotations

import os

from .base import ModelProvider
from .mock import DeterministicProvider, FixtureResponder
from .openai import OpenAIProvider


def get_provider(
    name: str | None = None,
    *,
    responder: FixtureResponder | None = None,
    model: str | None = None,
) -> ModelProvider:
    """Return the selected adapter without silently making a paid API call.

    `PROMPT_COURSE_PROVIDER` defaults to `mock`. Learners must explicitly set it
    to `openai` after configuring their own key.
    """

    selected = (name or os.getenv("PROMPT_COURSE_PROVIDER", "mock")).strip().lower()
    if selected in {"mock", "offline", "deterministic"}:
        return DeterministicProvider(responder)
    if selected == "openai":
        return OpenAIProvider(model=model)
    raise ValueError(f"Unknown provider {selected!r}; supported values are 'mock' and 'openai'")
