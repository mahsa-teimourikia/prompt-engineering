"""Explicit, user-supplied pricing calculations; no embedded provider prices."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .providers.base import Usage


@dataclass(frozen=True, slots=True)
class Pricing:
    input_per_million: float
    output_per_million: float
    source_url: str
    effective_date: date
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.input_per_million < 0 or self.output_per_million < 0:
            raise ValueError("pricing cannot be negative")
        if not self.source_url.startswith("https://"):
            raise ValueError("pricing requires an HTTPS source URL")


@dataclass(frozen=True, slots=True)
class CostEstimate:
    amount: float
    currency: str
    source_url: str
    effective_date: date
    usage_source: str


def estimate_cost(usage: Usage, pricing: Pricing) -> CostEstimate:
    if usage.input_tokens is None or usage.output_tokens is None:
        raise ValueError("input and output token counts are required")
    amount = (
        usage.input_tokens * pricing.input_per_million
        + usage.output_tokens * pricing.output_per_million
    ) / 1_000_000
    return CostEstimate(
        amount=amount,
        currency=pricing.currency,
        source_url=pricing.source_url,
        effective_date=pricing.effective_date,
        usage_source=usage.source,
    )
