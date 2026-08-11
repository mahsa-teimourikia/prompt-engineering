"""Token accounting with explicit measurement provenance."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping


_TOKEN_LIKE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def estimate_tokens(text: str) -> int:
    """Return a transparent tokenizer-independent approximation.

    Provider usage metadata must replace this estimate for billing or capacity
    decisions. The approximation is intended for controlled lab comparisons.
    """

    if not text:
        return 0
    lexical = len(_TOKEN_LIKE.findall(text))
    character_floor = (len(text) + 3) // 4
    return max(1, lexical, character_floor)


@dataclass(frozen=True, slots=True)
class ComponentUsage:
    component: str
    estimated_tokens: int


def measure_components(components: Mapping[str, str]) -> tuple[ComponentUsage, ...]:
    return tuple(
        ComponentUsage(component=name, estimated_tokens=estimate_tokens(text))
        for name, text in components.items()
    )
