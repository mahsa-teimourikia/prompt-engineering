"""Deterministic trust-boundary and authorization helpers."""

from __future__ import annotations

import html
import re

from pydantic import BaseModel, Field


class Principal(BaseModel):
    user_id: str
    tenant: str
    roles: set[str] = Field(default_factory=set)


class Action(BaseModel):
    name: str
    tenant: str
    requires_role: str


class Decision(BaseModel):
    allowed: bool
    reason_code: str


def authorize(principal: Principal, action: Action) -> Decision:
    """Authorize trusted application state, never model-generated text."""

    if principal.tenant != action.tenant:
        return Decision(allowed=False, reason_code="tenant_mismatch")
    if action.requires_role not in principal.roles:
        return Decision(allowed=False, reason_code="missing_role")
    return Decision(allowed=True, reason_code="ok")


def wrap_untrusted(text: str, label: str) -> str:
    """Wrap untrusted content while escaping tag delimiters inside it."""

    return f'<untrusted source="{html.escape(label, quote=True)}">{html.escape(text)}</untrusted>'


def instruction_like_score(text: str) -> float:
    """Heuristic detector, not a security boundary."""

    phrases = (
        "ignore previous",
        "ignore all previous",
        "system override",
        "you must now",
    )
    lowered = text.casefold()
    matches = sum(phrase in lowered for phrase in phrases)
    return min(1.0, 0.8 + (matches - 1) * 0.1) if matches else 0.0
