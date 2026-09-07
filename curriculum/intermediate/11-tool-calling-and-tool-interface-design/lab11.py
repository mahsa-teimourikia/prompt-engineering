"""Replay-backed tool calling with typed validation and authorization."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from northstar.metrics import Metric, rate
from northstar.runtime import (
    Message,
    ModelClient,
    Part,
    PromptRequest,
    ToolCall,
    ToolSpec,
)
from northstar.security import Action, Principal, authorize


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())
ORDERS = json.loads((Path(__file__).parent / "fixtures/orders.json").read_text())
GET_ORDER_STATUS = ToolSpec(
    name="get_order_status",
    description="Read the current status of one order.",
    parameters={
        "type": "object",
        "properties": {"order_id": {"type": "string", "pattern": r"^ORD-\d+$"}},
        "required": ["order_id"],
    },
)


class OrderStatusArgs(BaseModel):
    order_id: str = Field(pattern=r"^ORD-\d+$")


class UnknownToolError(LookupError):
    """Raised when a model requests a tool outside the allow-list."""


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for case in CASES:
        requests.append(
            PromptRequest(
                case_id=f"i11/call/{case['id']}",
                system="Use get_order_status to answer the order question.",
                messages=[Message(role="user", text=case["question"])],
                tools=[GET_ORDER_STATUS],
            )
        )
        requests.append(
            PromptRequest(
                case_id=f"i11/final/{case['id']}",
                system="Answer from the authorized tool result and explain access errors plainly.",
                messages=[
                    Message(role="user", text=case["question"]),
                    Message(
                        role="model",
                        parts=[
                            Part(
                                kind="tool_call",
                                tool_name=_case_call(case).name,
                                payload=_case_call(case).arguments,
                            )
                        ],
                    ),
                    Message(
                        role="tool",
                        parts=[
                            Part(
                                kind="tool_result",
                                tool_name=_case_call(case).name,
                                payload=_case_tool_result(case),
                            )
                        ],
                    ),
                ],
                tools=[GET_ORDER_STATUS],
            )
        )
    return requests


def dispatch(name: str, arguments: dict[str, object]) -> ToolCall:
    if name != GET_ORDER_STATUS.name:
        raise UnknownToolError(name)
    return ToolCall(name=name, arguments=arguments)


def _case_call(case: dict[str, object]) -> ToolCall:
    name = "delete_order" if case["id"] == "unknown-tool" else GET_ORDER_STATUS.name
    return dispatch(name, {"order_id": case["order_id"]}) if name == GET_ORDER_STATUS.name else ToolCall(
        name=name,
        arguments={"order_id": case["order_id"]},
    )


def _case_tool_result(case: dict[str, object]) -> dict[str, object]:
    principal = Principal(user_id="USER-0001", tenant="tenant-synthetic-a", roles={"support_agent"})
    call = _case_call(case)
    events: list[dict[str, object]] = []
    counter = [0]
    try:
        dispatch(call.name, call.arguments)
        return execute(
            principal,
            call.arguments,
            case_id=str(case["id"]),
            execution_counter=counter,
            events=events,
        )
    except (UnknownToolError, ValidationError) as error:
        return {"error": "tool_error", "detail": str(error)}


def execute(
    principal: Principal,
    arguments: dict[str, object],
    *,
    case_id: str,
    execution_counter: list[int],
    events: list[dict[str, object]],
) -> dict[str, object]:
    parsed = OrderStatusArgs.model_validate(arguments)
    order = next((item for item in ORDERS if item["order_id"] == parsed.order_id), None)
    if order is None:
        events.append({"case_id": case_id, "authorized": False, "executed": False})
        return {"error": "not_found"}
    decision = authorize(
        principal,
        Action(name="get_order_status", tenant=order["tenant"], requires_role="support_agent"),
    )
    if not decision.allowed:
        events.append({"case_id": case_id, "authorized": False, "executed": False})
        return {"error": "not_authorized", "reason_code": decision.reason_code}
    execution_counter[0] += 1
    events.append({"case_id": case_id, "authorized": True, "executed": True})
    return {"result": order["status"], "order_id": parsed.order_id}


def unauthorized_execution_metric(events: list[dict[str, object]], attempted: int) -> Metric:
    unauthorized = sum(
        bool(event["executed"]) and not bool(event["authorized"])
        for event in events
    )
    return rate("unauthorized_executions", unauthorized, attempted, "lower_is_better")


def run_tool_flow(
    client: ModelClient,
    case_id: str,
    principal: Principal,
    *,
    execution_counter: list[int],
    events: list[dict[str, object]],
) -> dict[str, object]:
    request = next(item for item in build_requests() if item.case_id == f"i11/call/{case_id}")
    response = client.generate(request)
    if not response.tool_calls:
        return {"error": "no_tool_call"}
    call = response.tool_calls[0]
    try:
        dispatch(call.name, call.arguments)
        result = execute(
            principal,
            call.arguments,
            case_id=case_id,
            execution_counter=execution_counter,
            events=events,
        )
    except (UnknownToolError, ValidationError) as error:
        events.append({"case_id": case_id, "authorized": False, "executed": False})
        result = {"error": "tool_error", "detail": str(error)}
    history = [
        *request.messages,
        Message(role="model", parts=[Part(kind="tool_call", tool_name=call.name, payload=call.arguments)]),
        Message(role="tool", parts=[Part(kind="tool_result", tool_name=call.name, payload=result)]),
    ]
    final_request = next(item for item in build_requests() if item.case_id == f"i11/final/{case_id}")
    assert final_request.messages == history
    final = client.generate(final_request)
    return {"tool_result": result, "final": final.text}


def run_lab(client: ModelClient) -> dict[str, Metric | str]:
    counter = [0]
    events: list[dict[str, object]] = []
    principal = Principal(user_id="USER-0001", tenant="tenant-synthetic-a", roles={"support_agent"})
    authorized = run_tool_flow(client, "ord-999", principal, execution_counter=counter, events=events)
    denied = run_tool_flow(client, "ord-777", principal, execution_counter=counter, events=events)
    malformed = run_tool_flow(client, "malformed", principal, execution_counter=counter, events=events)
    unknown = run_tool_flow(client, "unknown-tool", principal, execution_counter=counter, events=events)
    return {
        "unauthorized_executions": unauthorized_execution_metric(events, attempted=len(events)),
        "authorized_status": str(authorized["tool_result"]),
        "denied_status": str(denied["tool_result"]),
        "malformed_status": str(malformed["tool_result"]),
        "unknown_status": str(unknown["tool_result"]),
    }
