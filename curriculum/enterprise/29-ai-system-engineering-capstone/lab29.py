"""Capstone evidence and readiness gates for Course 29."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Mapping


REQUIRED_EVIDENCE = {
    "behavior_contract",
    "evaluation_report",
    "threat_model",
    "trace_sample",
    "rollback_plan",
    "owner",
}


@dataclass(frozen=True)
class EvidenceArtifact:
    location: str
    digest: str

    def valid(self, artifact_store: Mapping[str, str]) -> bool:
        content = artifact_store.get(self.location)
        return (
            bool(self.location.strip())
            and bool(re.fullmatch(r"[0-9a-f]{64}", self.digest))
            and content is not None
            and hashlib.sha256(content.encode()).hexdigest() == self.digest
        )


def evidence_artifact(location: str, content: str) -> EvidenceArtifact:
    """Describe expected evidence; readiness verifies it against trusted content."""

    return EvidenceArtifact(
        location=location,
        digest=hashlib.sha256(content.encode()).hexdigest(),
    )


@dataclass(frozen=True)
class CapstoneSubmission:
    project_id: str
    evidence: dict[str, EvidenceArtifact]
    critical_failures: int
    tests_passed: bool


@dataclass(frozen=True)
class Readiness:
    ready: bool
    missing: tuple[str, ...]
    invalid: tuple[str, ...]
    blockers: tuple[str, ...]


def evaluate_readiness(
    submission: CapstoneSubmission,
    artifact_store: Mapping[str, str],
) -> Readiness:
    missing = tuple(sorted(REQUIRED_EVIDENCE - set(submission.evidence)))
    invalid = tuple(
        sorted(
            key
            for key in REQUIRED_EVIDENCE & set(submission.evidence)
            if not isinstance(submission.evidence[key], EvidenceArtifact)
            or not submission.evidence[key].valid(artifact_store)
        )
    )
    blockers: list[str] = []
    if submission.critical_failures:
        blockers.append("critical_failures")
    if not submission.tests_passed:
        blockers.append("tests_failed")
    if missing:
        blockers.append("missing_evidence")
    if invalid:
        blockers.append("invalid_evidence")
    return Readiness(not blockers, missing, invalid, tuple(blockers))
