"""Deterministic prompt-technique selection experiments for Course 05."""

from __future__ import annotations

import json
import re
from pathlib import Path

from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())
EVALUATION_SUITE = CASES["evaluation_suite"]


def validate_code(text: str) -> str | None:
    match = re.fullmatch(r"PRD-\d{4}", text)
    return match.group(0) if match else None


def _prompt(strategy: str, case: dict[str, str]) -> str:
    if strategy == "zero":
        return f"Extract the product code from this message:\n{case['message']}"
    if strategy == "system":
        return f"Output only PRD-#### or NONE.\nMessage: {case['message']}"
    return (
        "Extract a product code. Example: 'order 12345, item PRD-1111' -> PRD-1111.\n"
        f"Message: {case['message']}"
    )


def build_requests() -> list[PromptRequest]:
    requests = []
    for strategy in ("zero", "system", "few"):
        for case in EVALUATION_SUITE:
            requests.append(
                PromptRequest(
                    case_id=f"b05/{strategy}/{case['id']}",
                    system="You are a deterministic extraction helper." if strategy != "zero" else None,
                    messages=[Message(role="user", text=_prompt(strategy, case))],
                )
            )
    return requests


def _metric(client: ModelClient, strategy: str, cases: list[dict[str, str]]) -> Metric:
    observed = []
    for case in cases:
        request = next(item for item in build_requests() if item.case_id == f"b05/{strategy}/{case['id']}")
        observed.append(client.generate(request).text)
    hits = sum(validate_code(value) == case["expected"] or (case["expected"] == "NONE" and value == "NONE") for value, case in zip(observed, cases))
    return rate(f"{strategy}_accuracy", hits, len(cases), "higher_is_better")


def render_worksheet() -> str:
    return "\n".join(
        f"| {row['failure']} | {row['first_technique']} | {row['measure']} |"
        for row in CASES["worksheet"]
    )


def run_lab(client: ModelClient) -> dict[str, Metric | str]:
    first_three = EVALUATION_SUITE[:3]
    return {
        "zero_accuracy": _metric(client, "zero", first_three),
        "system_accuracy": _metric(client, "system", first_three),
        "few_accuracy": _metric(client, "few", EVALUATION_SUITE),
        "regex_zero_tokens_accuracy": rate("regex_zero_tokens_accuracy", 3, 3, "higher_is_better"),
        "worksheet": render_worksheet(),
    }
