"""Deterministic canary routing and rollback evidence for Course 24."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


def route_version(request_id: str, *, canary_percent: int, rollback: bool = False) -> str:
    if not request_id:
        raise ValueError("stable request_id is required")
    if not 0 <= canary_percent <= 100:
        raise ValueError("canary_percent must be between 0 and 100")
    if rollback or canary_percent <= 0:
        return "stable"
    bucket = int(hashlib.sha256(request_id.encode()).hexdigest()[:8], 16) % 100
    return "canary" if bucket < canary_percent else "stable"


@dataclass(frozen=True)
class CanaryEvidence:
    requests: int
    failures: int
    critical_failures: int

    @property
    def failure_rate(self) -> float:
        return self.failures / self.requests if self.requests else 0.0


def should_rollback(evidence: CanaryEvidence, *, minimum_samples: int = 20, maximum_failure_rate: float = 0.05) -> tuple[bool, str]:
    if minimum_samples <= 0 or not 0 <= maximum_failure_rate <= 1:
        raise ValueError("invalid canary policy")
    if (
        evidence.requests < 0
        or evidence.failures < 0
        or evidence.critical_failures < 0
        or evidence.failures > evidence.requests
        or evidence.critical_failures > evidence.failures
    ):
        return True, "invalid_evidence"
    if evidence.critical_failures:
        return True, "critical_failure"
    if evidence.requests < minimum_samples:
        return False, "insufficient_samples"
    if evidence.failure_rate > maximum_failure_rate:
        return True, "failure_rate"
    return False, "within_budget"
