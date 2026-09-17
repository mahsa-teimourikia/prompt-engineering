"""Versioned behavior artifacts and release gates for Course 22."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class BehaviorArtifact:
    version: str
    prompt: str
    schema_version: str
    model_config: str
    dataset_version: str
    owner: str

    @property
    def digest(self) -> str:
        payload = json.dumps(self.__dict__, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()[:12]


@dataclass(frozen=True)
class GateInput:
    exact_passed: int
    total: int
    critical_failures: int
    schema_failures: int


def release_gate(metrics: GateInput, *, minimum_accuracy: float = 0.95) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    invalid_metrics = (
        metrics.total < 0
        or metrics.exact_passed < 0
        or metrics.exact_passed > metrics.total
        or metrics.critical_failures < 0
        or metrics.schema_failures < 0
        or not 0 <= minimum_accuracy <= 1
    )
    if invalid_metrics:
        reasons.append("invalid_metrics")
    elif metrics.total == 0:
        reasons.append("empty_evaluation")
    elif metrics.exact_passed / metrics.total < minimum_accuracy:
        reasons.append("accuracy_below_threshold")
    if metrics.critical_failures:
        reasons.append("critical_failures")
    if metrics.schema_failures:
        reasons.append("schema_failures")
    return not reasons, tuple(reasons)


def compare_artifacts(baseline: BehaviorArtifact, candidate: BehaviorArtifact) -> tuple[str, ...]:
    return tuple(
        field
        for field in baseline.__dataclass_fields__
        if getattr(baseline, field) != getattr(candidate, field)
    )
