"""Evidence and risk based trust calibration for Course 26."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ProposedAnswer:
    response: str
    confidence: float
    evidence_ids: tuple[str, ...]
    action_risk: Literal["low", "medium", "high"]


@dataclass(frozen=True)
class DeliveryDecision:
    state: Literal["answer", "clarify", "human_review", "blocked"]
    reason_code: str


def decide_delivery(answer: ProposedAnswer, known_evidence: set[str]) -> DeliveryDecision:
    """Route by observed evidence and impact; confidence alone never authorizes action."""

    if not answer.response.strip():
        return DeliveryDecision("blocked", "empty_response")
    if not answer.evidence_ids or not set(answer.evidence_ids).issubset(known_evidence):
        return DeliveryDecision("blocked", "unsupported_evidence")
    if answer.confidence < 0 or answer.confidence > 1:
        return DeliveryDecision("blocked", "invalid_confidence")
    if answer.action_risk == "high":
        return DeliveryDecision("human_review", "high_impact")
    if answer.confidence < 0.65:
        return DeliveryDecision("clarify", "low_confidence")
    return DeliveryDecision("answer", "supported")


def calibration_error(predictions: list[tuple[float, bool]]) -> float:
    if not predictions:
        raise ValueError("calibration requires labelled predictions")
    if any(not 0 <= confidence <= 1 for confidence, _ in predictions):
        raise ValueError("confidence values must be between 0 and 1")
    return sum(abs(confidence - float(correct)) for confidence, correct in predictions) / len(predictions)
