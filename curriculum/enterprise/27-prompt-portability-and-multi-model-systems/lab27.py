"""Provider-neutral contracts and safe fallback rules for Course 27."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from pydantic import BaseModel


class Summary(BaseModel):
    company: str
    revenue_trend: str
    risks: tuple[str, ...]


class Adapter(Protocol):
    name: str

    def summarize(self, text: str) -> Summary: ...


@dataclass
class FixtureAdapter:
    name: str
    available: bool = True
    schema_valid: bool = True

    def summarize(self, text: str) -> Summary:
        if not self.available:
            raise ConnectionError(f"{self.name}_unavailable")
        if not self.schema_valid:
            raise ValueError(f"{self.name}_schema_violation")
        if "drop" not in text.casefold():
            raise ValueError("fixture does not describe the expected scenario")
        return Summary(company="Acme Corp", revenue_trend="DOWN", risks=("supply chain",))


@dataclass(frozen=True)
class RoutedResult:
    value: Summary
    provider: str
    fallback_used: bool


def route(primary: Adapter, fallback: Adapter, text: str, *, operation_is_read_only: bool) -> RoutedResult:
    try:
        return RoutedResult(primary.summarize(text), primary.name, False)
    except (ConnectionError, TimeoutError):
        if not operation_is_read_only:
            raise RuntimeError("unsafe_fallback_for_side_effect")
        return RoutedResult(fallback.summarize(text), fallback.name, True)


def conformance(adapter: Adapter, fixtures: list[tuple[str, Summary]]) -> tuple[int, int]:
    if not fixtures:
        raise ValueError("conformance requires at least one fixture")
    passed = 0
    for text, expected in fixtures:
        try:
            passed += int(adapter.summarize(text) == expected)
        except (ValueError, ConnectionError, TimeoutError):
            pass
    return passed, len(fixtures)
