"""Policy-backed governance decisions for Course 25."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field


class GovernanceManifest(BaseModel):
    artifact_id: str
    artifact_digest: str = Field(min_length=12)
    owner: str
    risk_tier: Literal["low", "medium", "high"]
    handles_personal_data: bool
    intended_use: str
    prohibited_uses: tuple[str, ...]


@dataclass(frozen=True)
class Approval:
    approval_id: str
    artifact_id: str
    artifact_digest: str
    approver_id: str
    approver_role: str
    policy_version: str
    expires_at: int
    state: Literal["active", "revoked"]


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    reason_code: str


def governance_gate(
    manifest: GovernanceManifest,
    approvals: list[Approval],
    *,
    policy_version: str,
    now: int,
) -> GovernanceDecision:
    """Use trusted approval records; a flag inside model output is never authority."""

    if not manifest.owner or not manifest.intended_use:
        return GovernanceDecision(False, "incomplete_manifest")
    if manifest.intended_use in manifest.prohibited_uses:
        return GovernanceDecision(False, "prohibited_use")
    if manifest.risk_tier == "low" and not manifest.handles_personal_data:
        return GovernanceDecision(True, "low_risk")
    valid = any(
        approval.artifact_id == manifest.artifact_id
        and approval.artifact_digest == manifest.artifact_digest
        and bool(approval.approval_id)
        and bool(approval.approver_id)
        and approval.approver_role == "risk_board"
        and approval.policy_version == policy_version
        and approval.expires_at > now
        and approval.state == "active"
        for approval in approvals
    )
    return GovernanceDecision(valid, "approved" if valid else "approval_required")
