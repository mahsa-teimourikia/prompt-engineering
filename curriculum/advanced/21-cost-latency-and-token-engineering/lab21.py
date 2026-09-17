"""Quality-aware cost and latency experiments for Course 21."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyResult:
    name: str
    answer: str
    grounded: bool
    input_tokens: int
    output_tokens: int
    latency_ms: int
    cost_microunits: int


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def run_policy(name: str, context: str, question: str) -> PolicyResult:
    """Run a deterministic evidence-presence simulation, clearly labelled as such."""

    clause_present = "may terminate" in context.casefold()
    answer = "yes" if clause_present else "insufficient_evidence"
    tokens = estimate_tokens(context + question)
    return PolicyResult(
        name=name,
        answer=answer,
        grounded=clause_present,
        input_tokens=tokens,
        output_tokens=1 if clause_present else 5,
        latency_ms=40 + tokens * 2,
        cost_microunits=tokens * 3,
    )


def quality_gate(result: PolicyResult, expected: str) -> bool:
    grounding_matches = (
        not result.grounded
        if expected == "insufficient_evidence"
        else result.grounded
    )
    return result.answer == expected and grounding_matches


def dominates(left: PolicyResult, right: PolicyResult, *, expected: str) -> bool:
    """Return whether left is no worse on quality and strictly better on cost or latency."""

    quality_ok = quality_gate(left, expected) and quality_gate(right, expected)
    efficiency_ok = left.cost_microunits <= right.cost_microunits and left.latency_ms <= right.latency_ms
    strict = left.cost_microunits < right.cost_microunits or left.latency_ms < right.latency_ms
    return quality_ok and efficiency_ok and strict
