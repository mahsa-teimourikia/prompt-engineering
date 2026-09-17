"""Judge calibration and human-review utilities for Course 15."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Judgement:
    case_id: str
    score: int
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.case_id:
            raise ValueError("case_id is required")
        if not 1 <= self.score <= 5:
            raise ValueError("score must be between 1 and 5")


def rubric_judge(case_id: str, response: str) -> Judgement:
    """A transparent offline stand-in for a rubric judge, not a quality oracle."""

    lowered = response.casefold()
    reasons = []
    score = 1
    if any(word in lowered for word in ("sorry", "apolog")):
        score += 1
        reasons.append("acknowledges_harm")
    if any(word in lowered for word in ("replace", "refund", "resolve")):
        score += 2
        reasons.append("offers_resolution")
    if "immediately" in lowered or "today" in lowered:
        score += 1
        reasons.append("clear_timing")
    return Judgement(case_id, min(score, 5), tuple(reasons))


def agreement(judgements: Iterable[Judgement], human_scores: dict[str, int]) -> tuple[int, int]:
    """Return exact-agreement numerator and denominator."""

    rows = list(judgements)
    if not rows:
        raise ValueError("agreement requires at least one judgement")
    missing = [row.case_id for row in rows if row.case_id not in human_scores]
    if missing:
        raise KeyError(f"missing human labels: {missing}")
    if any(not 1 <= score <= 5 for score in human_scores.values()):
        raise ValueError("human scores must be between 1 and 5")
    return sum(row.score == human_scores[row.case_id] for row in rows), len(rows)


def pairwise_winner(left: str, right: str) -> str:
    """Compare without positional preference; ties are explicit."""

    left_score = rubric_judge("left", left).score
    right_score = rubric_judge("right", right).score
    if left_score == right_score:
        return "tie"
    return "left" if left_score > right_score else "right"


def requires_human_review(judgement: Judgement, *, high_impact: bool) -> bool:
    return high_impact or judgement.score < 4
