"""Explainable architecture selection and sensitivity analysis for Course 28."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Architecture:
    name: str
    determinism: int
    adaptability: int
    latency: int
    auditability: int
    operational_cost: int

    def __post_init__(self) -> None:
        scores = (
            self.determinism,
            self.adaptability,
            self.latency,
            self.auditability,
            self.operational_cost,
        )
        if any(not 1 <= score <= 5 for score in scores):
            raise ValueError("architecture scores must be between 1 and 5")


def weighted_score(architecture: Architecture, weights: dict[str, int]) -> int:
    """Score 1–5 benefits; ``operational_cost`` means cost efficiency (5 is best)."""

    values = architecture.__dict__
    unknown = set(weights) - (set(values) - {"name"})
    if unknown:
        raise KeyError(f"unknown criteria: {sorted(unknown)}")
    if not weights or any(weight < 0 for weight in weights.values()) or not any(weights.values()):
        raise ValueError("weights must contain at least one positive value and no negatives")
    return sum(int(values[name]) * weight for name, weight in weights.items())


def select_architecture(options: list[Architecture], weights: dict[str, int]) -> tuple[str, dict[str, int]]:
    if not options:
        raise ValueError("at least one architecture is required")
    if len({item.name for item in options}) != len(options):
        raise ValueError("architecture names must be unique")
    scores = {item.name: weighted_score(item, weights) for item in options}
    winner = max(options, key=lambda item: scores[item.name]).name
    return winner, scores


def sensitivity(options: list[Architecture], weight_sets: list[dict[str, int]]) -> dict[str, int]:
    if not weight_sets:
        raise ValueError("sensitivity requires at least one weight set")
    wins = {item.name: 0 for item in options}
    for weights in weight_sets:
        winner, _ = select_architecture(options, weights)
        wins[winner] += 1
    return wins
