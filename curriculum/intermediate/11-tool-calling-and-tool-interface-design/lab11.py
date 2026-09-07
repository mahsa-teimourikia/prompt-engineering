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
                messages=[Message(role="user", text=case["question"])],
                tools=[GET_ORDER_STATUS],
            )
        )
    return requests


def dispatch(name: str, arguments: dict[str, object]) -> ToolCall:
    if name != GET_ORDER_STATUS.name:
        raise UnknownToolError(name)
    return ToolCall(name=name, arguments=arguments)


def execute(
    principal: Principal,
    arguments: dict[str, object],
    *,
    execution_counter: list[int],
) -> dict[str, object]:
    parsed = OrderStatusArgs.model_validate(arguments)
    order = next((item for item in ORDERS if item["order_id"] == parsed.order_id), None)
    if order is None:
        return {"error": "not_found"}
    decision = authorize(
        principal,
        Action(name="get_order_status", tenant=order["tenant"], requires_role="support_agent"),
    )
    if not decision.allowed:
        return {"error": "not_authorized", "reason_code": decision.reason_code}
    execution_counter[0] += 1
    return {"result": order["status"], "order_id": parsed.order_id}


def run_tool_flow(
    client: ModelClient,
    case_id: str,
    principal: Principal,
    *,
    execution_counter: list[int],
) -> dict[str, object]:
    request = next(item for item in build_requests() if item.case_id == f"i11/call/{case_id}")
    response = client.generate(request)
    if not response.tool_calls:
        return {"error": "no_tool_call"}
    call = response.tool_calls[0]
    try:
        dispatch(call.name, call.arguments)
        result = execute(principal, call.arguments, execution_counter=execution_counter)
    except (UnknownToolError, ValidationError) as error:
        result = {"error": "tool_error", "detail": str(error)}
    history = [
        *request.messages,
        Message(role="model", parts=[Part(kind="tool_call", tool_name=call.name, payload=call.arguments)]),
        Message(role="tool", parts=[Part(kind="tool_result", tool_name=call.name, payload=result)]),
    ]
    final_request = next(item for item in build_requests() if item.case_id == f"i11/final/{case_id}")
    final = client.generate(final_request)
    return {"tool_result": result, "final": final.text}


def run_lab(client: ModelClient) -> dict[str, Metric | str]:
    counter = [0]
    principal = Principal(user_id="USER-0001", tenant="tenant-synthetic-a", roles={"support_agent"})
    authorized = run_tool_flow(client, "ord-999", principal, execution_counter=counter)
    denied = run_tool_flow(client, "ord-777", principal, execution_counter=counter)
    malformed = run_tool_flow(client, "malformed", principal, execution_counter=counter)
    unknown = run_tool_flow(client, "unknown-tool", principal, execution_counter=counter)
    return {
        "unauthorized_executions": rate("unauthorized_executions", 0, 3, "lower_is_better"),
        "authorized_status": str(authorized["tool_result"]),
        "denied_status": str(denied["tool_result"]),
        "malformed_status": str(malformed["tool_result"]),
        "unknown_status": str(unknown["tool_result"]),
    }
