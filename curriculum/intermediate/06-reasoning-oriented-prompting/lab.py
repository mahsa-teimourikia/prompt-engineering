"""Course 06 lab: observable reasoning artifacts for incident triage."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Literal

from pydantic import BaseModel, ConfigDict

from prompt_course import GenerationRequest, get_provider
from prompt_course.datasets import Case, load_jsonl
from prompt_course.token_usage import estimate_tokens


Action = Literal[
    "rollback",
    "escalate_database",
    "scale_capacity",
    "rotate_credentials",
    "collect_evidence",
    "monitor",
]
Strategy = Literal["direct", "decomposed", "planner_verifier", "self_consistency", "adaptive"]


class DecisionArtifact(BaseModel):
    """Auditable output fields, deliberately excluding private chain-of-thought."""

    model_config = ConfigDict(extra="forbid")
    action: Action
    evidence_ids: tuple[str, ...]
    checks: tuple[str, ...]
    assumptions: tuple[str, ...]
    needs_human: bool


@dataclass(frozen=True, slots=True)
class DecisionTrace:
    strategy: Strategy
    case_id: str
    slice: str
    expected: Action
    selected: Action
    candidates: tuple[Action, ...]
    artifact: DecisionArtifact
    correct: bool
    supported: bool
    calls: int
    tokens_estimated: int
    elapsed_seconds: float


SIGNAL_TO_ACTION: dict[str, Action] = {
    "deployment_regression": "rollback",
    "database_failure": "escalate_database",
    "cpu_saturation": "scale_capacity",
    "credential_compromise": "rotate_credentials",
    "recovered": "monitor",
}


def dataset_path() -> Path:
    return Path(__file__).parents[3] / "data" / "reasoning" / "incidents.jsonl"


def load_cases() -> list[Case]:
    return load_jsonl(dataset_path())


def action_from_signals(signals: list[str] | tuple[str, ...]) -> Action:
    actions = {SIGNAL_TO_ACTION[signal] for signal in signals if signal in SIGNAL_TO_ACTION}
    if actions == {"monitor"}:
        return "monitor"
    actions.discard("monitor")
    return next(iter(actions)) if len(actions) == 1 else "collect_evidence"


def direct_candidate(case: Case) -> Action:
    """A deliberately shallow lexical baseline over the incident narrative."""

    text = case.input.lower()
    if "credential" in text or "secret" in text:
        return "rotate_credentials"
    if "database" in text or "db " in text:
        return "escalate_database"
    if "cpu" in text or "capacity" in text:
        return "scale_capacity"
    if "deploy" in text or "release" in text:
        return "rollback"
    if "recovered" in text or "healthy again" in text:
        return "monitor"
    return "collect_evidence"


def _artifact(
    action: Action,
    evidence_ids: tuple[str, ...],
    checks: tuple[str, ...],
    assumptions: tuple[str, ...] = (),
) -> DecisionArtifact:
    return DecisionArtifact(
        action=action,
        evidence_ids=evidence_ids,
        checks=checks,
        assumptions=assumptions,
        needs_human=action in {"collect_evidence", "rotate_credentials"},
    )


def decide(case: Case, strategy: Strategy) -> tuple[DecisionArtifact, tuple[Action, ...], int]:
    signals = tuple(case.metadata.get("signals", ()))
    verified = tuple(case.metadata.get("verified_signals", ()))
    verified_action = action_from_signals(verified)

    if strategy == "direct":
        action = direct_candidate(case)
        return _artifact(action, (), ("classify narrative",)), (action,), 1

    decomposed_action = action_from_signals(signals)
    if strategy == "decomposed":
        assumptions = ("reported signals are verified",) if signals != verified else ()
        return (
            _artifact(
                decomposed_action,
                signals,
                ("enumerate hypotheses", "map signals to candidate action"),
                assumptions,
            ),
            (decomposed_action,),
            1,
        )

    if strategy == "planner_verifier":
        return (
            _artifact(
                verified_action,
                verified,
                ("enumerate hypotheses", "separate reported from verified evidence", "verify action support"),
            ),
            (decomposed_action, verified_action),
            2,
        )

    if strategy == "self_consistency":
        direct = direct_candidate(case)
        candidates = (direct, decomposed_action, verified_action, direct, decomposed_action)
        counts = Counter(candidates)
        action = max(counts, key=lambda item: (counts[item], -candidates.index(item)))
        return (
            _artifact(
                action,
                signals,
                ("sample five candidate decisions", "majority vote"),
                ("candidate agreement implies evidence support",),
            ),
            candidates,
            5,
        )

    if strategy == "adaptive":
        deterministic_action = case.metadata.get("deterministic_action")
        if deterministic_action:
            action = deterministic_action
            return (
                _artifact(action, verified, ("run deterministic health rule", "validate terminal state")),
                (action,),
                0,
            )
        return (
            _artifact(
                verified_action,
                verified,
                ("bound plan", "separate reported from verified evidence", "verify action support"),
            ),
            (decomposed_action, verified_action),
            2,
        )

    raise ValueError(f"unknown strategy: {strategy}")


def is_supported(case: Case, action: Action) -> bool:
    supported_action = action_from_signals(tuple(case.metadata.get("verified_signals", ())))
    return action == supported_action


def run_strategy(strategy: Strategy) -> list[DecisionTrace]:
    rows: list[DecisionTrace] = []
    for case in load_cases():
        started = perf_counter()
        artifact, candidates, calls = decide(case, strategy)
        elapsed = perf_counter() - started
        packet_tokens = estimate_tokens(case.input) + sum(estimate_tokens(item) for item in artifact.checks)
        rows.append(
            DecisionTrace(
                strategy=strategy,
                case_id=case.id,
                slice=case.slice,
                expected=case.expected,
                selected=artifact.action,
                candidates=candidates,
                artifact=artifact,
                correct=artifact.action == case.expected,
                supported=is_supported(case, artifact.action),
                calls=calls,
                tokens_estimated=packet_tokens * max(calls, 1),
                elapsed_seconds=elapsed,
            )
        )
    return rows


def metrics(rows: list[DecisionTrace]) -> dict[str, float]:
    if not rows:
        raise ValueError("rows must not be empty")
    escalation = [row for row in rows if row.expected == "collect_evidence"]
    return {
        "decision_accuracy": sum(row.correct for row in rows) / len(rows),
        "supported_decision_rate": sum(row.supported for row in rows) / len(rows),
        "safe_escalation_accuracy": sum(row.correct for row in escalation) / len(escalation),
        "mean_calls": sum(row.calls for row in rows) / len(rows),
        "mean_tokens_estimated": sum(row.tokens_estimated for row in rows) / len(rows),
        "mean_latency_ms": 1_000 * sum(row.elapsed_seconds for row in rows) / len(rows),
        "artifact_check_coverage": sum(bool(row.artifact.checks) for row in rows) / len(rows),
    }


def compare_strategies() -> list[dict[str, float | str]]:
    strategies: tuple[Strategy, ...] = (
        "direct",
        "decomposed",
        "planner_verifier",
        "self_consistency",
        "adaptive",
    )
    return [{"strategy": strategy, **metrics(run_strategy(strategy))} for strategy in strategies]


def failure_matrix(strategy: Strategy) -> list[dict[str, object]]:
    return [asdict(row) for row in run_strategy(strategy) if not row.correct]


def run_provider_case(case: Case):
    artifact, _, _ = decide(case, "adaptive")
    provider = get_provider(responder=lambda request: artifact.model_dump_json())
    request = GenerationRequest(
        instructions=(
            "Triage the incident using only verified evidence. Return the requested decision fields. "
            "Expose checks and assumptions, not private chain-of-thought. If evidence conflicts or is absent, collect evidence."
        ),
        input=f"INCIDENT (untrusted narrative):\n{case.input}",
        max_output_tokens=350,
        metadata={"case_id": case.id, "course": "06"},
    )
    return provider.generate_structured(request, DecisionArtifact)


# Compatibility with the earlier one-incident demonstration.
@dataclass(frozen=True)
class Incident:
    symptoms: tuple[str, ...]
    evidence: tuple[str, ...]


INCIDENT = Incident(("checkout failures", "timeouts"), ("database connection errors",))


def experiment(strategy: Strategy) -> list[dict[str, object]]:
    return [asdict(row) for row in run_strategy(strategy)]
