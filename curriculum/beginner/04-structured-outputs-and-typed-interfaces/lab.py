"""Course 04 lab: typed claim extraction and layered validation.

The deterministic candidates intentionally fail in different ways. Live mode
uses the same Pydantic contract through the shared OpenAI Responses adapter.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path
from time import perf_counter
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from prompt_course import GenerationRequest, get_provider
from prompt_course.datasets import Case, load_jsonl


class EmailContact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    channel: Literal["email"]
    value: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class PhoneContact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    channel: Literal["phone"]
    value: str = Field(pattern=r"^\+[1-9]\d{7,14}$")


Contact = Annotated[Union[EmailContact, PhoneContact], Field(discriminator="channel")]


class Claimant(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2)
    contact: Contact


class Money(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount: Decimal = Field(gt=0, decimal_places=2)
    currency: Literal["USD", "CAD", "EUR"]


class EvidenceRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence_id: str = Field(pattern=r"^[A-Z]+-\d+$")
    kind: Literal["invoice", "photo", "policy", "email"]
    supports: str = Field(min_length=5)


class CaseRecord(BaseModel):
    """Strict downstream interface; shape validity is not semantic validity."""

    model_config = ConfigDict(extra="forbid")
    case_id: str = Field(pattern=r"^CLM-\d{4}$")
    case_type: Literal["claim", "inquiry", "complaint"]
    claimant: Claimant
    incident_date: date
    claimed_amount: Money | None
    evidence: list[EvidenceRef] = Field(min_length=1)
    next_action: Literal["review", "request_information", "escalate"]
    missing_fields: list[str]


@dataclass(frozen=True, slots=True)
class StrategyResult:
    case_id: str
    slice: str
    strategy: str
    parse_success: bool
    schema_valid: bool
    semantic_correct: bool
    accepted: bool
    safe_decision: bool
    error_category: str | None
    elapsed_seconds: float
    raw: str


def dataset_path() -> Path:
    return Path(__file__).parents[3] / "data" / "structured_outputs" / "cases.jsonl"


def load_cases() -> list[Case]:
    return load_jsonl(dataset_path())


def _expected(case: Case) -> dict[str, Any]:
    return deepcopy(case.expected)


def candidate_for(case: Case, strategy: str) -> str:
    """Create measured deterministic candidates with realistic failure modes."""

    expected = _expected(case)
    index = int(case.id.split("-")[-1])
    if strategy == "free_text":
        return f"Open {expected['case_type']} {expected['case_id']} for {expected['claimant']['name']}."
    if strategy in {"json_prompt", "manual_schema", "pydantic_validation"}:
        failure = index % 5
        if failure == 0:
            return json.dumps(expected)[:-1]
        if failure == 1:
            expected["priority"] = "urgent"
        elif failure == 2:
            expected["case_type"] = "refund"
        elif failure == 3:
            del expected["claimant"]
        else:
            amount = expected.get("claimed_amount")
            if amount:
                amount["amount"] = str(Decimal(str(amount["amount"])) + Decimal("10.00"))
            else:
                expected["next_action"] = "review"
        return json.dumps(expected)
    if strategy == "provider_native":
        # Schema-constrained generation can still produce the wrong meaning.
        if index % 7 == 0:
            expected["next_action"] = (
                "review" if expected["next_action"] != "review" else "escalate"
            )
        return json.dumps(expected)
    raise ValueError(f"unknown strategy: {strategy}")


def manual_schema_errors(value: Any) -> list[str]:
    """A deliberately transparent subset of JSON Schema-like checks."""

    required = {
        "case_id",
        "case_type",
        "claimant",
        "incident_date",
        "claimed_amount",
        "evidence",
        "next_action",
        "missing_fields",
    }
    if not isinstance(value, dict):
        return ["root must be an object"]
    errors = []
    if set(value) != required:
        errors.append("root fields do not match contract")
    if value.get("case_type") not in {"claim", "inquiry", "complaint"}:
        errors.append("case_type enum violation")
    if value.get("next_action") not in {"review", "request_information", "escalate"}:
        errors.append("next_action enum violation")
    if not isinstance(value.get("evidence"), list) or not value.get("evidence"):
        errors.append("evidence must be a non-empty list")
    return errors


def semantic_errors(record: CaseRecord, case: Case) -> list[str]:
    """Compare meaning against labelled evidence, independent of shape."""

    expected = _expected(case)
    actual = record.model_dump(mode="json")
    errors: list[str] = []
    for field in ("case_id", "case_type", "incident_date", "next_action", "missing_fields"):
        if actual[field] != expected[field]:
            errors.append(f"{field} differs from labelled record")
    if actual["claimant"] != expected["claimant"]:
        errors.append("claimant differs from labelled record")
    if actual["claimed_amount"] != expected["claimed_amount"]:
        errors.append("claimed_amount differs from labelled record")
    actual_ids = {item["evidence_id"] for item in actual["evidence"]}
    expected_ids = {item["evidence_id"] for item in expected["evidence"]}
    if actual_ids != expected_ids:
        errors.append("evidence identifiers differ from labelled record")
    return errors


def evaluate_candidate(case: Case, strategy: str, raw: str | None = None) -> StrategyResult:
    started = perf_counter()
    raw = raw if raw is not None else candidate_for(case, strategy)
    parse_success = schema_valid = semantic_correct = accepted = False
    error_category: str | None = None
    try:
        value = json.loads(raw)
        parse_success = True
    except json.JSONDecodeError:
        value = None
        error_category = "parse"

    record: CaseRecord | None = None
    if parse_success:
        try:
            record = CaseRecord.model_validate(value)
            schema_valid = True
        except ValidationError:
            error_category = "schema"
        if record is not None:
            semantic_correct = not semantic_errors(record, case)
            if not semantic_correct:
                error_category = "semantic"

    if strategy == "json_prompt":
        accepted = parse_success
    elif strategy == "manual_schema":
        accepted = parse_success and not manual_schema_errors(value)
    elif strategy in {"pydantic_validation", "provider_native"}:
        accepted = schema_valid and semantic_correct
    safe_decision = accepted == semantic_correct
    return StrategyResult(
        case_id=case.id,
        slice=case.slice,
        strategy=strategy,
        parse_success=parse_success,
        schema_valid=schema_valid,
        semantic_correct=semantic_correct,
        accepted=accepted,
        safe_decision=safe_decision,
        error_category=error_category,
        elapsed_seconds=perf_counter() - started,
        raw=raw,
    )


def run_experiment(strategies: tuple[str, ...] | None = None) -> list[StrategyResult]:
    selected = strategies or (
        "free_text",
        "json_prompt",
        "manual_schema",
        "pydantic_validation",
        "provider_native",
    )
    return [evaluate_candidate(case, strategy) for strategy in selected for case in load_cases()]


def summarize(results: list[StrategyResult]) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for strategy in sorted({result.strategy for result in results}):
        group = [result for result in results if result.strategy == strategy]
        rows.append(
            {
                "strategy": strategy,
                "cases": len(group),
                "parse_success": sum(item.parse_success for item in group) / len(group),
                "schema_valid": sum(item.schema_valid for item in group) / len(group),
                "semantic_correct": sum(item.semantic_correct for item in group) / len(group),
                "safe_decision": sum(item.safe_decision for item in group) / len(group),
                "mean_validation_ms": 1_000
                * sum(item.elapsed_seconds for item in group)
                / len(group),
            }
        )
    return rows


def bounded_repair(raw: str) -> str | None:
    """Remove unknown root fields once; never invent missing business facts."""

    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(value, dict):
        return None
    allowed = set(CaseRecord.model_fields)
    repaired = {key: item for key, item in value.items() if key in allowed}
    try:
        CaseRecord.model_validate(repaired)
    except ValidationError:
        return None
    return json.dumps(repaired)


def run_provider_case(case: Case):
    """Run one typed extraction offline or through the learner-selected provider."""

    expected_json = json.dumps(_expected(case))
    provider = get_provider(responder=lambda request: expected_json)
    request = GenerationRequest(
        instructions=(
            "Extract only facts present in the document. Preserve evidence IDs. "
            "Use request_information when required facts are missing."
        ),
        input=case.input,
        max_output_tokens=900,
        metadata={"case_id": case.id, "schema": "CaseRecord-v1"},
    )
    return provider.generate_structured(request, CaseRecord)
