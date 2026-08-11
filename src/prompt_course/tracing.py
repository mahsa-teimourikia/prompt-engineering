"""Structured trace events that expose decisions without chain-of-thought."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any, Literal, Mapping


EventKind = Literal["input", "decision", "model", "retrieval", "tool", "validation", "error"]


@dataclass(frozen=True, slots=True)
class TraceEvent:
    sequence: int
    elapsed_seconds: float
    stage: str
    kind: EventKind
    summary: str
    attributes: Mapping[str, Any] = field(default_factory=dict)


class TraceCollector:
    def __init__(self) -> None:
        self._started = perf_counter()
        self._events: list[TraceEvent] = []

    @property
    def events(self) -> tuple[TraceEvent, ...]:
        return tuple(self._events)

    def record(
        self,
        stage: str,
        kind: EventKind,
        summary: str,
        **attributes: Any,
    ) -> TraceEvent:
        event = TraceEvent(
            sequence=len(self._events) + 1,
            elapsed_seconds=perf_counter() - self._started,
            stage=stage,
            kind=kind,
            summary=summary,
            attributes=attributes,
        )
        self._events.append(event)
        return event

    def as_dicts(self) -> list[dict[str, Any]]:
        return [asdict(event) for event in self._events]
