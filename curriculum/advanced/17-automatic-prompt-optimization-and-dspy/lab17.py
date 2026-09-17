"""Bounded, reproducible prompt search for Course 17."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class SearchCase:
    text: str
    expected: str
    split: str


@dataclass(frozen=True)
class PromptCandidate:
    name: str
    extractor: Callable[[str], str]


def last_token_baseline(text: str) -> str:
    return text.rstrip(".").split()[-1]


def after_marker(text: str) -> str:
    marker = "city:"
    lowered = text.casefold()
    if marker not in lowered:
        return last_token_baseline(text)
    start = lowered.index(marker) + len(marker)
    return text[start:].split(";")[0].strip()


def exact_accuracy(candidate: PromptCandidate, cases: Iterable[SearchCase]) -> tuple[int, int]:
    rows = list(cases)
    return sum(candidate.extractor(row.text) == row.expected for row in rows), len(rows)


def select_on_development(
    candidates: Iterable[PromptCandidate],
    cases: Iterable[SearchCase],
    *,
    max_candidates: int = 8,
) -> PromptCandidate:
    development = [case for case in cases if case.split == "development"]
    if not development:
        raise ValueError("prompt search requires a development split")
    candidate_rows = list(candidates)
    if not candidate_rows:
        raise ValueError("prompt search requires at least one candidate")
    if not 1 <= len(candidate_rows) <= max_candidates:
        raise ValueError("candidate search budget exceeded")
    ranked = sorted(
        candidate_rows,
        key=lambda candidate: (-exact_accuracy(candidate, development)[0], candidate.name),
    )
    return ranked[0]


def evaluate_holdout(candidate: PromptCandidate, cases: Iterable[SearchCase]) -> tuple[int, int]:
    holdout = [case for case in cases if case.split == "holdout"]
    if not holdout:
        raise ValueError("evaluation requires a protected holdout split")
    return exact_accuracy(candidate, holdout)
