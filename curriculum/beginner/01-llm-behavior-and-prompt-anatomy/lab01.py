"""Deterministic experiments for Course 01."""

from __future__ import annotations

import json
from typing import Literal
from pathlib import Path

from pydantic import BaseModel

from northstar.contracts import parse_structured
from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest, estimate_tokens


class SupportClassification(BaseModel):
    category: Literal["refund", "shipping", "account", "unknown"]


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())

EVIDENCE = (
    "Approved Policies:\n"
    "- Refunds: Allowed within 30 days of purchase.\n"
    "- Shipping: Track via the carrier link in your email.\n"
    "- Account: Reset passwords via the login page.\n"
)
INSTRUCTION = (
    "Classify the support request using ONLY the approved evidence. "
    "If the message doesn't match the evidence clearly, return 'unknown'."
)


def _messages(case: dict[str, str], *, position: str = "first") -> list[Message]:
    if position == "middle":
        padding = "The customer is a highly valued member. Please be polite.\n" * 10
        text = f"{INSTRUCTION}\n{padding}{EVIDENCE}\n{padding}Message: {case['message']}"
        return [Message(role="user", text=text)]
    return [Message(role="user", text=f"{EVIDENCE}\nMessage: {case['message']}")]


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for case in CASES:
        requests.append(
            PromptRequest(
                case_id=f"b01/baseline/{case['id']}",
                system=INSTRUCTION,
                messages=_messages(case),
                response_schema=SupportClassification,
                temperature=0.0,
            )
        )
        requests.append(
            PromptRequest(
                case_id=f"b01/middle/{case['id']}",
                system=INSTRUCTION,
                messages=_messages(case, position="middle"),
                response_schema=SupportClassification,
                temperature=0.0,
            )
        )
    requests.extend(
        [
            PromptRequest(
                case_id="b01/sampling/temp-0",
                system=INSTRUCTION,
                messages=_messages(CASES[-1]),
                response_schema=SupportClassification,
                temperature=0.0,
            ),
            PromptRequest(
                case_id="b01/sampling/temp-09",
                system=INSTRUCTION,
                messages=_messages(CASES[-1]),
                response_schema=SupportClassification,
                temperature=0.9,
            ),
            PromptRequest(
                case_id="b01/missing/weak",
                system="Classify the support request.",
                messages=[Message(role="user", text="Message: Can I return my order?")],
                response_schema=SupportClassification,
            ),
            PromptRequest(
                case_id="b01/missing/abstain",
                system="Use only supplied evidence. If evidence is missing, return unknown.",
                messages=[Message(role="user", text="Message: Can I return my order?")],
                response_schema=SupportClassification,
            ),
            PromptRequest(
                case_id="b01/structure/roles",
                system=INSTRUCTION,
                messages=[Message(role="user", text=CASES[0]["message"])],
                response_schema=SupportClassification,
            ),
            PromptRequest(
                case_id="b01/structure/concatenated",
                messages=[
                    Message(
                        role="user",
                        text=f"{INSTRUCTION}\n{CASES[0]['message']}",
                    )
                ],
                response_schema=SupportClassification,
            ),
        ]
    )
    return requests


def _response(client: ModelClient, request: PromptRequest) -> SupportClassification:
    response = client.generate(request)
    parsed = response.parsed
    if parsed is not None:
        return parsed
    result = parse_structured(SupportClassification, response.text)
    if not result.ok:
        raise ValueError(result.error)
    return result.value


def _accuracy(
    client: ModelClient,
    prefix: str,
    expected: list[str],
) -> Metric:
    observed = [
        _response(client, request).category
        for request in build_requests()
        if request.case_id.startswith(prefix)
    ]
    return rate(
        f"{prefix.replace('/', '_')}_accuracy",
        sum(actual == wanted for actual, wanted in zip(observed, expected)),
        len(expected),
        "higher_is_better",
    )


def run_lab(client: ModelClient) -> dict[str, Metric | tuple[str, str]]:
    baseline = _accuracy(client, "b01/baseline/", [case["expected"] for case in CASES])
    middle = _accuracy(client, "b01/middle/", [case["expected"] for case in CASES])
    temp_zero = _response(client, build_requests()[-6]).category
    temp_nine = _response(client, build_requests()[-5]).category
    weak = _response(client, build_requests()[-4]).category
    abstain = _response(client, build_requests()[-3]).category
    role_request, concatenated_request = build_requests()[-2:]
    return {
        "baseline_accuracy": baseline,
        "middle_accuracy": middle,
        "temperature_comparison": (temp_zero, temp_nine),
        "weak_missing_evidence": rate("weak_missing_evidence", weak == "refund", 1, "lower_is_better"),
        "abstention_missing_evidence": rate("abstention_missing_evidence", abstain == "unknown", 1, "higher_is_better"),
        "padding_tokens": rate(
            "padding_tokens",
            estimate_tokens("The customer is a sandbox account. " * 10),
            1,
            "lower_is_better",
            unit="estimated_tokens",
        ),
        "role_fingerprints": (role_request.fingerprint(), concatenated_request.fingerprint()),
    }
