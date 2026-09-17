"""Portable model-adapter comparison for Course 20."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel


class Entity(BaseModel):
    company: str
    year: int
    industry: str


@dataclass(frozen=True)
class ModelProfile:
    name: str
    supports_schema: bool
    context_limit: int
    latency_ms: int
    cost_microunits: int

    def __post_init__(self) -> None:
        if min(self.context_limit, self.latency_ms, self.cost_microunits) < 0:
            raise ValueError("profile limits and measurements cannot be negative")


@dataclass(frozen=True)
class Trial:
    model: str
    correct: bool
    contract_valid: bool
    native_schema: bool
    latency_ms: int
    cost_microunits: int


def normalized_extract(profile: ModelProfile, text: str) -> Entity:
    """Deterministic adapter simulation with one provider-neutral output contract."""

    estimated_tokens = max(1, (len(text) + 3) // 4)
    if estimated_tokens > profile.context_limit:
        raise ValueError("context_limit_exceeded")
    if "1998" not in text or "Google" not in text:
        raise ValueError("fixture is outside the adapter simulation")
    return Entity(company="Google", year=1998, industry="search")


def run_trial(profile: ModelProfile, text: str, expected: Entity) -> Trial:
    try:
        result = normalized_extract(profile, text)
    except ValueError:
        return Trial(
            profile.name,
            False,
            False,
            profile.supports_schema,
            profile.latency_ms,
            profile.cost_microunits,
        )
    return Trial(
        profile.name,
        result == expected,
        True,
        profile.supports_schema,
        profile.latency_ms,
        profile.cost_microunits,
    )


def choose_profile(trials: list[Trial], *, latency_budget_ms: int, cost_budget: int) -> str | None:
    eligible = [trial for trial in trials if trial.correct and trial.contract_valid and trial.latency_ms <= latency_budget_ms and trial.cost_microunits <= cost_budget]
    return min(eligible, key=lambda trial: (trial.cost_microunits, trial.latency_ms)).model if eligible else None
