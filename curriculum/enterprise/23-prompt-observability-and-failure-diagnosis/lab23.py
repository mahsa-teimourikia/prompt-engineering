"""Privacy-aware traces and deterministic diagnosis for Course 23."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal


EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)


def redact(value: str) -> str:
    return EMAIL.sub("[REDACTED_EMAIL]", value)


def redact_value(value: Any, *, key: str = "") -> Any:
    if key.casefold() in {"api_key", "authorization", "password", "secret", "token"}:
        return "[REDACTED_SECRET]"
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, dict):
        return {
            item_key: redact_value(item, key=str(item_key))
            for item_key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    return value


@dataclass(frozen=True)
class Span:
    trace_id: str
    name: str
    status: Literal["ok", "error"]
    duration_ms: int
    attributes: dict[str, Any] = field(default_factory=dict)


def safe_span(trace_id: str, name: str, status: str, duration_ms: int, attributes: dict[str, Any]) -> Span:
    if not trace_id or not name:
        raise ValueError("trace_id and span name are required")
    if status not in {"ok", "error"}:
        raise ValueError("status must be ok or error")
    if duration_ms < 0:
        raise ValueError("duration_ms cannot be negative")
    cleaned = redact_value(attributes)
    return Span(trace_id, name, status, duration_ms, cleaned)


def diagnose(spans: list[Span]) -> str:
    """Classify the first observable failing layer; do not infer hidden reasoning."""

    if not spans:
        return "missing_trace"
    for span in spans:
        if span.status == "error":
            return f"{span.name}_error"
        if span.attributes.get("evidence_fresh") is False:
            return "stale_evidence"
        if span.attributes.get("schema_valid") is False:
            return "schema_violation"
    return "no_observed_failure"
