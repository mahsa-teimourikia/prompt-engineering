"""Deterministic evaluation primitives for Course 14."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable, Literal


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    text: str
    expected: str
    slice: str
    severity: Literal["normal", "critical"] = "normal"

    def __post_init__(self) -> None:
        if self.severity not in {"normal", "critical"}:
            raise ValueError("severity must be normal or critical")


@dataclass(frozen=True)
class EvalReport:
    passed: int
    total: int
    critical_failures: tuple[str, ...]
    by_slice: dict[str, tuple[int, int]]

    @property
    def accuracy(self) -> float:
        return self.passed / self.total if self.total else 0.0


def evaluate(classifier: Callable[[str], str], cases: Iterable[EvalCase]) -> EvalReport:
    """Score exact labels while retaining denominators and critical failures."""

    rows = list(cases)
    if not rows:
        raise ValueError("evaluation requires at least one labelled case")
    passed = 0
    critical: list[str] = []
    slices: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for case in rows:
        ok = classifier(case.text) == case.expected
        passed += int(ok)
        slices[case.slice][0] += int(ok)
        slices[case.slice][1] += 1
        if not ok and case.severity == "critical":
            critical.append(case.case_id)
    return EvalReport(
        passed=passed,
        total=len(rows),
        critical_failures=tuple(critical),
        by_slice={name: tuple(values) for name, values in sorted(slices.items())},
    )


def release_allowed(report: EvalReport, *, minimum_accuracy: float = 0.8) -> bool:
    if not 0 <= minimum_accuracy <= 1:
        raise ValueError("minimum_accuracy must be between 0 and 1")
    if report.total <= 0 or not 0 <= report.passed <= report.total:
        return False
    if any(total <= 0 or not 0 <= passed <= total for passed, total in report.by_slice.values()):
        return False
    if sum(total for _, total in report.by_slice.values()) != report.total:
        return False
    return report.accuracy >= minimum_accuracy and not report.critical_failures


def keyword_baseline(text: str) -> str:
    lowered = text.casefold()
    if "refund" in lowered or "money back" in lowered:
        return "refund"
    if "broken" in lowered or "login" in lowered or "fix" in lowered:
        return "technical"
    return "other"


def intent_candidate(text: str) -> str:
    lowered = text.casefold()
    if any(phrase in lowered for phrase in ("want my money back", "request a refund")):
        return "refund"
    if any(word in lowered for word in ("broken", "login", "fix", "snapped")):
        return "technical"
    return "other"
