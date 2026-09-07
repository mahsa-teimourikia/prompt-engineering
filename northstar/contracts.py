"""Deterministic output contracts shared by the lessons."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel


class ParseResult:
    """Result of parsing and validating a structured model response."""

    def __init__(
        self,
        ok: bool,
        value: Any = None,
        error_code: str | None = None,
        error: str | None = None,
    ) -> None:
        self.ok = ok
        self.value = value
        self.error_code = error_code
        self.error = error

    def __repr__(self) -> str:
        return (
            f"ParseResult(ok={self.ok!r}, value={self.value!r}, "
            f"error_code={self.error_code!r}, error={self.error!r})"
        )


class Violation(BaseModel):
    """One deterministic constraint violation."""

    code: str
    detail: str


def _strip_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines.pop()
        return "\n".join(lines).strip()
    return stripped


def parse_structured(schema: type[BaseModel], text: str) -> ParseResult:
    """Parse JSON and return a classified result without raising."""

    if not text.strip():
        return ParseResult(False, error_code="empty", error="response is empty")
    try:
        data = json.loads(_strip_fence(text))
    except json.JSONDecodeError as exc:
        return ParseResult(False, error_code="not_json", error=str(exc))
    try:
        value = schema.model_validate(data)
    except Exception as exc:
        return ParseResult(False, error_code="schema_violation", error=str(exc))
    return ParseResult(True, value=value)


def check_constraints(
    text: str,
    *,
    max_words: int | None = None,
    forbidden_phrases: tuple[str, ...] = (),
    required_phrases: tuple[str, ...] = (),
    allowed_values: set[str] | None = None,
) -> list[Violation]:
    """Check simple deterministic text constraints."""

    violations: list[Violation] = []
    if max_words is not None and len(text.split()) > max_words:
        violations.append(
            Violation(
                code="max_words",
                detail=f"response has more than {max_words} words",
            )
        )
    lowered = text.casefold()
    for phrase in forbidden_phrases:
        if phrase.casefold() in lowered:
            violations.append(
                Violation(
                    code="forbidden_phrase",
                    detail=f"forbidden phrase present: {phrase}",
                )
            )
    for phrase in required_phrases:
        if phrase.casefold() not in lowered:
            violations.append(
                Violation(
                    code="required_phrase",
                    detail=f"required phrase missing: {phrase}",
                )
            )
    if allowed_values is not None and text not in allowed_values:
        violations.append(
            Violation(
                code="allowed_value",
                detail=f"value is not one of {sorted(allowed_values)}",
            )
        )
    return violations


ABSTAIN_VALUES = {"unknown", "INSUFFICIENT_DATA", "abstain"}


def is_abstention(value: Any) -> bool:
    """Return whether a value is one of the shared abstention markers."""

    return isinstance(value, str) and value in ABSTAIN_VALUES
