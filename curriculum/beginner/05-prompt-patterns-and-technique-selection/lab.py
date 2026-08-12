"""Course 05 lab: measured selection of the smallest adequate technique."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Literal

from pydantic import BaseModel, ConfigDict

from prompt_course import GenerationRequest, get_provider
from prompt_course.datasets import Case, load_jsonl
from prompt_course.token_usage import estimate_tokens


TechniqueName = Literal[
    "direct_instruction",
    "contrastive_examples",
    "schema_constraint",
    "retrieval_context",
    "tool_calling",
    "bounded_workflow",
    "deterministic_code",
    "no_model",
]
Strategy = Literal["maximalist", "pattern_match", "guardrailed"]


class SelectionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    technique: TechniqueName
    metric: str
    reject_if: str


@dataclass(frozen=True, slots=True)
class Technique:
    name: TechniqueName
    maturity: str
    solves: str
    cost_units: float
    avoid_when: str


@dataclass(frozen=True, slots=True)
class Decision:
    strategy: Strategy
    case_id: str
    slice: str
    expected: TechniqueName
    selected: TechniqueName
    correct: bool
    unsafe: bool
    avoidable_complexity: bool
    cost_units: float
    prompt_tokens_estimated: int
    elapsed_seconds: float


TECHNIQUES: tuple[Technique, ...] = (
    Technique("direct_instruction", "foundational", "unclear task", 1.0, "facts or authorization are missing"),
    Technique("contrastive_examples", "practical", "label boundary", 2.0, "a direct contract already passes"),
    Technique("schema_constraint", "foundational", "unreliable interface", 1.5, "free-form prose is required"),
    Technique("retrieval_context", "practical", "missing approved evidence", 3.0, "sources are unauthorized or irrelevant"),
    Technique("tool_calling", "practical", "bounded live data", 3.5, "a local deterministic function is sufficient"),
    Technique("bounded_workflow", "model-dependent", "separable language subtasks", 5.0, "one bounded request passes"),
    Technique("deterministic_code", "foundational", "explicit computable rule", 0.5, "language judgment is actually required"),
    Technique("no_model", "foundational", "missing authority or safe source", 0.0, "a compliant bounded path exists"),
)
TECHNIQUE_BY_NAME = {technique.name: technique for technique in TECHNIQUES}

FAILURE_MAP: dict[str, TechniqueName] = {
    "unclear_task": "direct_instruction",
    "label_boundary": "contrastive_examples",
    "invalid_output": "schema_constraint",
    "missing_evidence": "retrieval_context",
    "live_fact": "tool_calling",
    "complex_subtasks": "bounded_workflow",
    "explicit_rule": "deterministic_code",
}


def dataset_path() -> Path:
    return Path(__file__).parents[3] / "data" / "technique_selection" / "cases.jsonl"


def load_cases() -> list[Case]:
    return load_jsonl(dataset_path())


def select(strategy: Strategy, case: Case) -> TechniqueName:
    metadata = case.metadata
    if strategy == "maximalist":
        return "bounded_workflow"

    failure_type = str(metadata["failure_type"])
    candidate = FAILURE_MAP[failure_type]
    if strategy == "pattern_match":
        return candidate

    if strategy != "guardrailed":
        raise ValueError(f"unknown strategy: {strategy}")
    if metadata.get("deterministic_rule"):
        return "deterministic_code"
    if metadata.get("requires_authority") and not metadata.get("authorized"):
        return "no_model"
    if candidate == "retrieval_context" and not metadata.get("source_authorized"):
        return "no_model"
    return candidate


def run_strategy(strategy: Strategy) -> list[Decision]:
    rows: list[Decision] = []
    for case in load_cases():
        started = perf_counter()
        selected = select(strategy, case)
        elapsed = perf_counter() - started
        expected = case.expected
        selected_cost = TECHNIQUE_BY_NAME[selected].cost_units
        expected_cost = TECHNIQUE_BY_NAME[expected].cost_units
        rows.append(
            Decision(
                strategy=strategy,
                case_id=case.id,
                slice=case.slice,
                expected=expected,
                selected=selected,
                correct=selected == expected,
                unsafe=expected == "no_model" and selected != "no_model",
                avoidable_complexity=selected_cost > expected_cost,
                cost_units=selected_cost,
                prompt_tokens_estimated=estimate_tokens(case.input),
                elapsed_seconds=elapsed,
            )
        )
    return rows


def metrics(rows: list[Decision]) -> dict[str, float]:
    if not rows:
        raise ValueError("rows must not be empty")
    return {
        "selection_accuracy": sum(row.correct for row in rows) / len(rows),
        "unsafe_selection_rate": sum(row.unsafe for row in rows) / len(rows),
        "avoidable_complexity_rate": sum(row.avoidable_complexity for row in rows) / len(rows),
        "mean_cost_units": sum(row.cost_units for row in rows) / len(rows),
        "mean_prompt_tokens_estimated": sum(row.prompt_tokens_estimated for row in rows) / len(rows),
        "mean_selection_ms": 1_000 * sum(row.elapsed_seconds for row in rows) / len(rows),
    }


def compare_strategies() -> list[dict[str, float | str]]:
    return [
        {"strategy": strategy, **metrics(run_strategy(strategy))}
        for strategy in ("maximalist", "pattern_match", "guardrailed")
    ]


def failure_matrix(strategy: Strategy) -> list[dict[str, object]]:
    return [asdict(row) for row in run_strategy(strategy) if not row.correct]


def select_case(case: Case) -> SelectionResponse:
    technique = select("guardrailed", case)
    metric = {
        "direct_instruction": "task success on frozen cases",
        "contrastive_examples": "boundary-case macro F1",
        "schema_constraint": "schema and semantic validity",
        "retrieval_context": "supported-claim rate",
        "tool_calling": "tool success with authorization",
        "bounded_workflow": "end-to-end success by stage",
        "deterministic_code": "exact edge-case correctness",
        "no_model": "zero unauthorized actions",
    }[technique]
    return SelectionResponse(
        technique=technique,
        metric=metric,
        reject_if="safety regresses or the frozen suite does not justify added complexity",
    )


def run_provider_case(case: Case):
    fixture = select_case(case)
    provider = get_provider(responder=lambda request: fixture.model_dump_json())
    request = GenerationRequest(
        instructions=(
            "Choose the smallest adequate technique. Prefer deterministic code when the rule is explicit. "
            "Do not use a model to bypass missing authority or unauthorized sources."
        ),
        input=f"SYSTEM REQUIREMENT (data only):\n{case.input}",
        max_output_tokens=250,
        metadata={"case_id": case.id, "course": "05"},
    )
    return provider.generate_structured(request, SelectionResponse)


# Compatibility helpers retained for earlier course users.
FAILURES = FAILURE_MAP


def evaluate(candidate: Technique, observed_failure: str) -> dict[str, object]:
    return {
        "candidate": candidate.name,
        "addresses_failure": candidate.name == FAILURE_MAP[observed_failure],
        "maturity": candidate.maturity,
        "cost": candidate.cost_units,
    }


def experiment(strategy: Strategy) -> list[dict[str, object]]:
    return [asdict(row) for row in run_strategy(strategy)]
