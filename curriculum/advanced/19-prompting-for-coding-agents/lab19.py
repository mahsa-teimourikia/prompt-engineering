"""Software-change contract validation for Course 19."""

from __future__ import annotations

from pathlib import PurePosixPath

from pydantic import BaseModel, Field


class ChangeContract(BaseModel):
    problem: str = Field(min_length=10)
    allowed_files: tuple[str, ...] = Field(min_length=1)
    test_command: tuple[str, ...] = Field(min_length=1)
    acceptance: tuple[str, ...] = Field(min_length=1)
    allow_network: bool = False


class ProposedChange(BaseModel):
    files_to_read: tuple[str, ...]
    files_to_write: tuple[str, ...]
    command: tuple[str, ...]


def validate_plan(contract: ChangeContract, plan: ProposedChange) -> tuple[str, ...]:
    """Return machine-readable violations; natural-language promises are not enforcement."""

    allowed = {str(PurePosixPath(path)) for path in contract.allowed_files}
    violations: list[str] = []
    if any(str(PurePosixPath(path)) not in allowed for path in plan.files_to_read):
        violations.append("read_scope")
    if any(str(PurePosixPath(path)) not in allowed for path in plan.files_to_write):
        violations.append("write_scope")
    if tuple(plan.command) != tuple(contract.test_command):
        violations.append("command_not_approved")
    if any(part in {"curl", "wget"} for part in plan.command) and not contract.allow_network:
        violations.append("network_not_approved")
    return tuple(dict.fromkeys(violations))


def completion_allowed(contract: ChangeContract, *, tests_passed: bool, diff_files: tuple[str, ...]) -> bool:
    return (
        tests_passed
        and bool(diff_files)
        and set(diff_files).issubset(set(contract.allowed_files))
    )
