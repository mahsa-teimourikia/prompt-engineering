"""Replay-backed reasoning, verification, and self-consistency experiments."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())


class TriageRecommendation(BaseModel):
    reasoning_steps: list[str] = Field(default_factory=list)
    recommended_action: str
    confidence: str


class VerificationResult(BaseModel):
    is_safe: bool
    reasoning: str


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for case in CASES:
        logs = case["logs"]
        requests.extend(
            [
                PromptRequest(
                    case_id=f"i06/naive/{case['id']}",
                    system="You are an SRE. Recommend one triage action from the incident logs.",
                    messages=[Message(role="user", text=logs)],
                    response_schema=TriageRecommendation,
                ),
                PromptRequest(
                    case_id=f"i06/cot/{case['id']}",
                    system=(
                        "Analyze the incident step by step, name the root cause, "
                        "then recommend a reversible action."
                    ),
                    messages=[Message(role="user", text=logs)],
                    response_schema=TriageRecommendation,
                ),
                PromptRequest(
                    case_id=f"i06/verifier/{case['id']}",
                    system=(
                        "Verify whether the proposed action is safe for automatic "
                        "execution. Reject actions that change capacity or restart databases."
                    ),
                    messages=[
                        Message(
                            role="user",
                            text=f"Proposed action: {case['expected_action']}",
                        )
                    ],
                    response_schema=VerificationResult,
                ),
            ]
        )
    requests.append(
        PromptRequest(
            case_id="i06/verifier/optimistic",
            system="Verify whether the proposed action is safe for automatic execution.",
            messages=[Message(role="user", text="Restart DB_MAIN to clear the pool")],
            response_schema=VerificationResult,
        )
    )
    for sample, action in enumerate(("Increase DB connection pool ceiling", "Increase DB connection pool ceiling", "Restart the application service"), start=1):
        requests.append(
            PromptRequest(
                case_id=f"i06/self-consistency/sample-{sample}",
                system="Analyze the incident and recommend one action.",
                messages=[Message(role="user", text=CASES[0]["logs"])],
                response_schema=TriageRecommendation,
                temperature=0.7,
            )
        )
    return requests


def root_cause_named(steps: list[str], keyword: str) -> bool:
    return keyword.casefold() in " ".join(steps).casefold()


def classify_action_risk(action: str) -> Literal["safe", "requires_approval"]:
    if re.search(r"\b(scale|increase|pool|restart|database|drop|delete)\b", action, re.I):
        return "requires_approval"
    return "safe"


def decide(action: str, verifier: VerificationResult) -> Literal["auto_execute", "human_approval"]:
    if classify_action_risk(action) == "safe" and verifier.is_safe:
        return "auto_execute"
    return "human_approval"


def majority_vote(actions: list[str]) -> tuple[str, float]:
    winner = max(set(actions), key=actions.count)
    return winner, actions.count(winner) / len(actions)


def _parsed(client: ModelClient, request: PromptRequest, schema: type[BaseModel]):
    response = client.generate(request)
    if response.parsed is not None:
        return response.parsed
    return schema.model_validate_json(response.text)


def run_lab(client: ModelClient) -> dict[str, Metric | tuple[str, float] | str]:
    naive = [
        _parsed(client, next(r for r in build_requests() if r.case_id == f"i06/naive/{case['id']}"), TriageRecommendation)
        for case in CASES
    ]
    cot = [
        _parsed(client, next(r for r in build_requests() if r.case_id == f"i06/cot/{case['id']}"), TriageRecommendation)
        for case in CASES
    ]
    verifications = [
        _parsed(client, next(r for r in build_requests() if r.case_id == f"i06/verifier/{case['id']}"), VerificationResult)
        for case in CASES
    ]
    root_cause_metric = rate(
        "root_cause_named",
        sum(root_cause_named(result.reasoning_steps, case["root_cause_keyword"]) for result, case in zip(cot, CASES)),
        len(CASES),
        "higher_is_better",
    )
    naive_root_cause = rate(
        "naive_root_cause_named",
        sum(root_cause_named(result.reasoning_steps, case["root_cause_keyword"]) for result, case in zip(naive, CASES)),
        len(CASES),
        "higher_is_better",
    )
    decisions = [
        decide(result.recommended_action, verifier)
        for result, verifier in zip(cot, verifications)
    ]
    optimistic_request = next(r for r in build_requests() if r.case_id == "i06/verifier/optimistic")
    optimistic = _parsed(client, optimistic_request, VerificationResult)
    actions = [
        next(r for r in build_requests() if r.case_id == f"i06/self-consistency/sample-{sample}")
        for sample in (1, 2, 3)
    ]
    samples = [_parsed(client, request, TriageRecommendation).recommended_action for request in actions]
    return {
        "root_cause_named": root_cause_metric,
        "naive_root_cause_named": naive_root_cause,
        "verifier_decisions": ",".join(decisions),
        "optimistic_decision": decide("Restart DB_MAIN to clear the pool", optimistic),
        "self_consistency": majority_vote(samples),
    }
