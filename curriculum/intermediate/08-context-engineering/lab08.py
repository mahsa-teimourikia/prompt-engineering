"""Replay-backed context packet and deterministic policy-control experiments."""

from __future__ import annotations

import json
import re
from pathlib import Path

from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest, estimate_tokens
from northstar.security import instruction_like_score


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())
USER_DATA = CASES[0]["user_data"]


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for case in CASES:
        requests.extend(
            [
                PromptRequest(
                    case_id=f"i08/naive/{case['id']}",
                    system="You are the approval bot.",
                    messages=[Message(role="user", text=case["naive_user"])],
                ),
                PromptRequest(
                    case_id=f"i08/engineered/{case['id']}",
                    system="You are the approval bot. Evaluate the user request against the strict policy.",
                    messages=[Message(role="user", text=case["engineered_user"])],
                ),
            ]
        )
    return requests


def requested_nodes(text: str) -> int:
    match = re.search(r"Requested Nodes:\s*(\d+)", text, re.I)
    return int(match.group(1)) if match else 0


def policy_allows(requested: int, limit: int = 5) -> bool:
    return 0 < requested <= limit


def decide(model_answer: str, requested: int) -> str:
    return "approved" if model_answer.casefold() == "yes" and policy_allows(requested) else "rejected"


def build_packet(sections: list[tuple[str, str, int]], budget_tokens: int) -> str:
    selected: list[tuple[str, str, int]] = []
    for section in sorted(sections, key=lambda item: -item[2]):
        candidate = selected + [section]
        rendered = "\n".join(f"[{name}]\n{text}" for name, text, _ in candidate)
        if estimate_tokens(rendered) <= budget_tokens:
            selected.append(section)
    return "\n".join(f"[{name}]\n{text}" for name, text, _ in selected)


def run_lab(client: ModelClient) -> dict[str, Metric | bool | str]:
    engineered_answers: list[str] = []
    decisions: list[str] = []
    for case in CASES:
        request = next(item for item in build_requests() if item.case_id == f"i08/engineered/{case['id']}")
        engineered_answers.append(client.generate(request).text)
        decisions.append(decide(engineered_answers[-1], requested_nodes(case["user_data"])))
    sections = [
        ("policy", "At most 5 nodes may be requested.", 100),
        ("customer request", USER_DATA, 50),
        ("chat history", "A long low-priority conversation history.", 1),
    ]
    packet = build_packet(sections, budget_tokens=15)
    return {
        "policy_decisions": ",".join(decisions),
        "approved_cases": rate(
            "approved_cases",
            decisions.count("approved"),
            len(CASES),
            "higher_is_better",
        ),
        "injection_score": instruction_like_score(USER_DATA),
        "policy_retained": "[policy]" in packet,
        "chat_history_dropped": "[chat history]" not in packet,
    }
