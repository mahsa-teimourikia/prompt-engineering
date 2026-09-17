"""Bounded agent routing and execution contracts for Course 18."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field

from northstar.security import Action, Principal, authorize


ORDER_TENANTS = {"O1": "northstar", "O2": "other"}


class AgentTask(BaseModel):
    task_id: str
    tenant: str
    kind: Literal["lookup", "summarize"]
    payload: dict[str, str]
    max_steps: int = Field(ge=1, le=4)


@dataclass(frozen=True)
class AgentResult:
    status: Literal["completed", "blocked", "budget_exhausted", "invalid"]
    reason_code: str
    output: str = ""


def route(task: AgentTask, principal: Principal) -> AgentResult:
    """Authorize before exposing a capability or reading task payloads."""

    decision = authorize(
        principal,
        Action(name=task.kind, tenant=task.tenant, requires_role="support_agent"),
    )
    if not decision.allowed:
        return AgentResult("blocked", decision.reason_code)
    if task.max_steps < 2:
        return AgentResult("budget_exhausted", "step_budget")
    if task.kind == "lookup":
        order_id = task.payload.get("order_id")
        if not order_id:
            return AgentResult("invalid", "missing_order_id")
        resource_tenant = ORDER_TENANTS.get(order_id)
        if resource_tenant is None:
            return AgentResult("invalid", "order_not_found")
        if resource_tenant != principal.tenant:
            return AgentResult("blocked", "resource_tenant_mismatch")
        return AgentResult("completed", "ok", f"order {order_id}: in_transit")
    text = task.payload.get("text", "")
    if not text:
        return AgentResult("invalid", "missing_text")
    return AgentResult("completed", "ok", " ".join(text.split()[:8]))


def architecture_cost(*, agents: int, model_calls: int, handoffs: int) -> int:
    if min(agents, model_calls, handoffs) < 0:
        raise ValueError("architecture counts cannot be negative")
    return agents * 2 + model_calls + handoffs * 2
