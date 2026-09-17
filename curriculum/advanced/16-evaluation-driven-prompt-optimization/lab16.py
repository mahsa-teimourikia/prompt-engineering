"""Holdout-aware prompt-policy comparison for Course 16."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Literal


@dataclass(frozen=True)
class ExtractionCase:
    case_id: str
    headline: str
    company: str
    sentiment: str
    split: Literal["development", "holdout"]

    def __post_init__(self) -> None:
        if self.split not in {"development", "holdout"}:
            raise ValueError("split must be development or holdout")


@dataclass(frozen=True)
class CandidateScore:
    name: str
    company_correct: int
    sentiment_correct: int
    joint_correct: int
    total: int

    @property
    def joint_accuracy(self) -> float:
        return self.joint_correct / self.total if self.total else 0.0


def baseline_policy(headline: str) -> tuple[str, str]:
    company = headline.split()[0].lstrip("$")
    sentiment = "positive" if any(word in headline.casefold() for word in ("profit", "rallies", "growth")) else "negative"
    return company, sentiment


ALIASES = {"GOOG": "Google", "MSFT": "Microsoft"}


def alias_policy(headline: str) -> tuple[str, str]:
    company, sentiment = baseline_policy(headline)
    return ALIASES.get(company, company), sentiment


def score(name: str, policy: Callable[[str], tuple[str, str]], cases: Iterable[ExtractionCase]) -> CandidateScore:
    rows = list(cases)
    if not rows:
        raise ValueError("cannot score an empty split")
    predictions = [policy(row.headline) for row in rows]
    pairs = list(zip(predictions, rows))
    return CandidateScore(
        name=name,
        company_correct=sum(actual[0] == row.company for actual, row in pairs),
        sentiment_correct=sum(actual[1] == row.sentiment for actual, row in pairs),
        joint_correct=sum(actual == (row.company, row.sentiment) for actual, row in pairs),
        total=len(rows),
    )


def split_cases(cases: Iterable[ExtractionCase], split: str) -> list[ExtractionCase]:
    if split not in {"development", "holdout"}:
        raise ValueError("split must be development or holdout")
    return [case for case in cases if case.split == split]
