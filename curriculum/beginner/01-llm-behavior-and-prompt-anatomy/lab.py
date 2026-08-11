"""Credential-free experiments for Course 01: LLM behavior and prompt anatomy.

This module is deliberately a transparent simulator, not a claim about a
provider's internal implementation. It lets learners change one part of an
inference request at a time and measure the resulting behavior contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Literal


Intent = Literal["refund", "shipping", "account", "unknown"]


@dataclass(frozen=True)
class PromptPacket:
    """The inspectable parts of one model request."""

    instruction: str
    user_message: str
    examples: tuple[tuple[str, Intent], ...] = ()
    evidence_position: Literal["first", "middle", "last"] = "first"
    evidence_available: bool = True
    temperature: float = 0.0


@dataclass(frozen=True)
class Observation:
    case_id: str
    expected: Intent
    observed: Intent
    supported: bool
    token_estimate: int


CASES: tuple[tuple[str, str, Intent], ...] = (
    ("clear-refund", "My order arrived yesterday. Can I return it?", "refund"),
    ("clear-shipping", "Where is order 42?", "shipping"),
    ("clear-account", "Please update the email on my account.", "account"),
    ("ambiguous-payment", "I was charged and need help.", "unknown"),
)


def _keywords(message: str) -> Intent:
    text = message.lower()
    if any(word in text for word in ("return", "refund", "arrived")):
        return "refund"
    if any(word in text for word in ("where", "tracking", "order 42")):
        return "shipping"
    if any(word in text for word in ("email", "account", "address")):
        return "account"
    return "unknown"


def classify(packet: PromptPacket, *, seed: int = 7) -> Intent:
    """Return a bounded observable result for a controlled teaching experiment.

    Ambiguity, missing evidence, position, and temperature affect only this
    synthetic decision rule. A real provider experiment must capture the same
    packet fields, model snapshot, raw response, validation result, tokens, and
    latency before conclusions are made.
    """

    intent = _keywords(packet.user_message)
    if not packet.evidence_available and intent == "refund":
        return "unknown"
    if "classify" not in packet.instruction.lower():
        return "unknown"
    if packet.evidence_position == "middle" and intent == "refund":
        # A visible proxy for a position-sensitivity test, not a model claim.
        intent = "unknown"
    if packet.temperature > 0 and intent != "unknown":
        probability = min(packet.temperature * 0.35, 0.45)
        if Random(seed).random() < probability:
            intent = "unknown"
    return intent


def token_estimate(packet: PromptPacket) -> int:
    """A reproducible approximation for comparing packet composition only."""

    text = " ".join(
        [packet.instruction, packet.user_message]
        + [f"{question} {label}" for question, label in packet.examples]
    )
    return max(1, len(text.split()))


def run_suite(packet_factory) -> list[Observation]:
    """Run the same frozen cases through a supplied packet factory."""

    observations: list[Observation] = []
    for case_id, message, expected in CASES:
        packet = packet_factory(message)
        observed = classify(packet)
        observations.append(
            Observation(
                case_id=case_id,
                expected=expected,
                observed=observed,
                supported=packet.evidence_available or observed != "refund",
                token_estimate=token_estimate(packet),
            )
        )
    return observations


def score(observations: list[Observation]) -> dict[str, float]:
    """Report accuracy, support rate, and average request-size proxy."""

    total = len(observations)
    if not total:
        raise ValueError("observations must not be empty")
    return {
        "accuracy": sum(item.expected == item.observed for item in observations) / total,
        "support_rate": sum(item.supported for item in observations) / total,
        "mean_token_estimate": sum(item.token_estimate for item in observations) / total,
    }
