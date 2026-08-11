"""Typed dataset helpers with stable, leakage-resistant splits."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping


Split = Literal["development", "validation", "held_out"]


@dataclass(frozen=True, slots=True)
class Case:
    id: str
    input: str
    expected: Any
    slice: str = "normal"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.input:
            raise ValueError("case id and input are required")


def deterministic_split(case_id: str, seed: int = 17) -> Split:
    """Assign a stable 60/20/20 split without depending on input order."""

    bucket = int(hashlib.sha256(f"{seed}:{case_id}".encode()).hexdigest()[:8], 16) % 10
    if bucket < 6:
        return "development"
    if bucket < 8:
        return "validation"
    return "held_out"


def load_jsonl(path: str | Path) -> list[Case]:
    cases: list[Case] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                cases.append(Case(**row))
            except (json.JSONDecodeError, TypeError) as exc:
                raise ValueError(f"Invalid JSONL case at {path}:{line_number}") from exc
    return cases


def slice_counts(cases: Iterable[Case]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for case in cases:
        counts[case.slice] = counts.get(case.slice, 0) + 1
    return dict(sorted(counts.items()))
