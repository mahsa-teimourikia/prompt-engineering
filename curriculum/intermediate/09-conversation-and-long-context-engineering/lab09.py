"""Replay-backed conversation memory and state-management experiments."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel, Field

from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest, estimate_tokens


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())


class UserState(BaseModel):
    active_order_id: str | None = Field(
        default=None,
        description="The active order ID if the user provided one, otherwise null.",
    )
    user_intent: str | None = Field(
        default=None,
        description="What the user is trying to accomplish.",
    )
    issue: str | None = None
    needs_confirmation: bool = False


def contains_order_id(text: str) -> str | None:
    match = re.search(r"\bORD-\d+\b", text)
    return match.group(0) if match else None


def _history_text(message: dict[str, str] | str) -> str:
    if isinstance(message, dict):
        return f"{message['role']}: {message['content']}"
    return message


def sliding_window(
    history: list[dict[str, str] | str],
    budget_tokens: int,
) -> list[str]:
    selected: list[str] = []
    for message in reversed(history):
        candidate = [_history_text(message)] + selected
        if estimate_tokens("\n".join(candidate)) > budget_tokens:
            break
        selected = candidate
    return selected


def merge_state(old: UserState, new: UserState) -> UserState:
    different = (
        old.active_order_id is not None
        and new.active_order_id is not None
        and old.active_order_id != new.active_order_id
    )
    return UserState(
        active_order_id=new.active_order_id or old.active_order_id,
        issue=new.issue or old.issue,
        needs_confirmation=old.needs_confirmation or new.needs_confirmation or different,
    )


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for index, case in enumerate(CASES, start=1):
        history = [_history_text(item) for item in case["history"]]
        context = "\n".join(sliding_window(case["history"], 10_000))
        current_request = case.get(
            "current_request",
            "Okay great. Anyway, can you give me an update on my order?",
        )
        if index == 1:
            summary = (
                "The user needs help with order ORD-5592. "
                "They also asked about shipping to Alaska and Hawaii."
            )
            state = UserState(
                active_order_id="ORD-5592",
                user_intent="Check order status",
            )
            strategy_messages = {
                "window": (
                    "You are a helpful assistant.\nRecent Chat History:\n"
                    f"{context}\n\nUser: {current_request}\n"
                ),
                "summary": (
                    "You are a helpful assistant.\nConversation Summary: "
                    f"{summary}\nRecent Chat History:\n{context}\n\n"
                    f"User: {current_request}\n"
                ),
                "state": (
                    "You are a helpful assistant.\nUser State:\n"
                    f"{state.model_dump_json(indent=2)}\n\n"
                    f"Recent Chat History:\n{context}\n\nUser: {current_request}\n"
                ),
            }
        else:
            strategy_messages = {
                strategy: case[strategy] for strategy in ("window", "summary", "state")
            }
        requests.append(
            PromptRequest(
                case_id=f"i09/state/extract-turn-{index}",
                system="Extract durable user state from the conversation.",
                messages=[Message(role="user", text=history[0])],
                response_schema=UserState,
            )
        )
        for strategy in ("window", "summary", "state"):
            requests.append(
                PromptRequest(
                    case_id=f"i09/{strategy}/{case['id']}",
                    system="You are a helpful assistant.",
                    messages=[Message(role="user", text=strategy_messages[strategy])],
                )
            )
    return requests


def run_lab(client: ModelClient) -> dict[str, Metric | bool]:
    retained: dict[str, int] = {}
    for strategy in ("window", "summary", "state"):
        answers = [
            client.generate(
                next(item for item in build_requests() if item.case_id == f"i09/{strategy}/{case['id']}")
            ).text
            for case in CASES
        ]
        retained[strategy] = sum(contains_order_id(answer) is not None for answer in answers)
    extracted = [
        client.generate(
            next(item for item in build_requests() if item.case_id == f"i09/state/extract-turn-{index}")
        ).parsed
        for index in range(1, len(CASES) + 1)
    ]
    return {
        "window_order_id_retained": rate("window_order_id_retained", retained["window"], len(CASES), "higher_is_better"),
        "summary_order_id_retained": rate("summary_order_id_retained", retained["summary"], len(CASES), "higher_is_better"),
        "state_order_id_retained": rate("state_order_id_retained", retained["state"], len(CASES), "higher_is_better"),
        "state_extractions_valid": all(isinstance(state, UserState) for state in extracted),
    }
