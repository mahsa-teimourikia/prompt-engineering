"""Replay-backed decomposition and policy-gated workflow experiments."""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from northstar.contracts import check_constraints
from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())
ORDERS = json.loads((Path(__file__).parent / "fixtures/orders.json").read_text())
TODAY = date(2026, 3, 1)


class Extraction(BaseModel):
    order_id: str = Field(description="The extracted order ID, or 'UNKNOWN'")
    customer_intent: str = Field(
        default="refund",
        description="What the customer wants (e.g. refund, exchange)",
    )


class Draft(BaseModel):
    answer: str


@dataclass
class WorkflowTrace:
    steps: list[dict[str, object]] = field(default_factory=list)
    terminal_state: Literal["drafted", "clarification_required"] = "clarification_required"


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for case in CASES:
        requests.append(
            PromptRequest(
                case_id=f"i07/naive/{case['id']}",
                system="",
                messages=[Message(role="user", text=case["original_naive_prompt"])],
                response_schema=Draft,
            )
        )
        requests.append(
            PromptRequest(
                case_id=f"i07/extract/{case['id']}",
                system="",
                messages=[Message(role="user", text=case["extract_user"])],
                response_schema=Extraction,
            )
        )
        if case["expected_terminal"] == "drafted":
            eligible = refund_eligible(case["expected_order_id"])
            draft_user = case["original_draft_prompt"].format(
                customer_intent="refund",
                is_eligible=eligible == "eligible",
            )
            requests.append(
                PromptRequest(
                    case_id=f"i07/draft/{case['id']}",
                    system="You are a customer support bot.",
                    messages=[Message(role="user", text=draft_user)],
                    response_schema=Draft,
                )
            )
    return requests


def refund_eligible(order_id: str, today: date = TODAY) -> Literal["eligible", "ineligible", "not_found"]:
    order = next((item for item in ORDERS if item["order_id"] == order_id), None)
    if order is None:
        return "not_found"
    age = (today - date.fromisoformat(order["ordered_on"])).days
    return "eligible" if age <= 30 else "ineligible"


def _request(client: ModelClient, case_id: str, schema: type[BaseModel]):
    request = next(item for item in build_requests() if item.case_id == case_id)
    response = client.generate(request)
    return response.parsed or schema.model_validate_json(response.text)


def run_workflow(client: ModelClient, email: str) -> WorkflowTrace:
    case = next(item for item in CASES if item["email"] == email)
    extracted = _request(client, f"i07/extract/{case['id']}", Extraction)
    trace = WorkflowTrace()
    trace.steps.append(
        {
            "node": "extract",
            "input_digest": hashlib.sha256(email.encode()).hexdigest(),
            "output": extracted.order_id,
            "terminal_state": None,
        }
    )
    if extracted.order_id == "UNKNOWN":
        trace.terminal_state = "clarification_required"
        trace.steps[-1]["terminal_state"] = trace.terminal_state
        return trace
    eligibility = refund_eligible(extracted.order_id)
    trace.steps.append(
        {"node": "policy", "input_digest": extracted.order_id, "output": eligibility, "terminal_state": None}
    )
    draft = _request(client, f"i07/draft/{case['id']}", Draft)
    trace.steps.append(
        {"node": "draft", "input_digest": eligibility, "output": draft.answer, "terminal_state": "drafted"}
    )
    trace.terminal_state = "drafted"
    return trace


def run_lab(client: ModelClient) -> dict[str, Metric | list[str]]:
    naive = _request(client, "i07/naive/original-email", Draft)
    traces = [run_workflow(client, case["email"]) for case in CASES]
    violations = 0
    for case, trace in zip(CASES, traces):
        if trace.terminal_state != "drafted":
            continue
        draft = str(trace.steps[-1]["output"]).casefold()
        eligibility = refund_eligible(case["expected_order_id"])
        if eligibility == "ineligible" and "approved" in draft:
            violations += 1
        if eligibility == "eligible" and "outside the 30-day" in draft:
            violations += 1
    naive_violation = int(bool(check_constraints(naive.answer, forbidden_phrases=("approved",))))
    drafted_cases = [case for case in CASES if case["expected_terminal"] == "drafted"]
    baseline_cases = [case for case in CASES if case["id"] == "original-email"]
    return {
        "policy_violations": rate(
            "policy_violations",
            violations,
            len(drafted_cases),
            "lower_is_better",
        ),
        "naive_policy_violations": rate(
            "naive_policy_violations",
            naive_violation,
            len(baseline_cases),
            "lower_is_better",
        ),
        "terminal_states": [trace.terminal_state for trace in traces],
    }
