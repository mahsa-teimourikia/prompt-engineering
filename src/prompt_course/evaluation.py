"""Small transparent evaluation primitives used before framework abstractions."""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass
from statistics import mean
from typing import Any, Callable, Iterable, Mapping

from .datasets import Case


System = Callable[[Case], Any]
Grader = Callable[[Any, Case], Mapping[str, float | bool]]


@dataclass(frozen=True, slots=True)
class EvaluationRecord:
    case_id: str
    slice: str
    output: Any
    scores: Mapping[str, float]


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    records: tuple[EvaluationRecord, ...]
    overall: Mapping[str, float]
    by_slice: Mapping[str, Mapping[str, float]]


def _normalize_score(value: float | bool) -> float:
    score = float(value)
    if not 0.0 <= score <= 1.0:
        raise ValueError(f"evaluation score must be in [0, 1], received {score}")
    return score


def evaluate_cases(cases: Iterable[Case], system: System, grader: Grader) -> EvaluationSummary:
    records: list[EvaluationRecord] = []
    for case in cases:
        output = system(case)
        scores = {name: _normalize_score(value) for name, value in grader(output, case).items()}
        if not scores:
            raise ValueError("grader must return at least one metric")
        records.append(EvaluationRecord(case.id, case.slice, output, scores))
    if not records:
        raise ValueError("evaluation requires at least one case")

    metric_names = sorted({name for record in records for name in record.scores})
    overall = {
        name: mean(record.scores[name] for record in records if name in record.scores)
        for name in metric_names
    }
    grouped: dict[str, list[EvaluationRecord]] = defaultdict(list)
    for record in records:
        grouped[record.slice].append(record)
    by_slice = {
        slice_name: {
            name: mean(record.scores[name] for record in slice_records if name in record.scores)
            for name in metric_names
            if any(name in record.scores for record in slice_records)
        }
        for slice_name, slice_records in sorted(grouped.items())
    }
    return EvaluationSummary(tuple(records), overall, by_slice)


def bootstrap_interval(
    values: Iterable[float],
    *,
    confidence: float = 0.95,
    samples: int = 2_000,
    seed: int = 17,
) -> tuple[float, float]:
    """Return a deterministic percentile bootstrap interval for the mean."""

    data = tuple(float(value) for value in values)
    if not data:
        raise ValueError("bootstrap interval requires values")
    if not 0 < confidence < 1 or samples < 100:
        raise ValueError("confidence must be in (0, 1) and samples must be >= 100")
    rng = random.Random(seed)
    estimates = sorted(mean(rng.choice(data) for _ in data) for _ in range(samples))
    tail = (1 - confidence) / 2
    lower = estimates[int(tail * (samples - 1))]
    upper = estimates[int((1 - tail) * (samples - 1))]
    return lower, upper
