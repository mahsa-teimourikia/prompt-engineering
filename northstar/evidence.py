"""Evidence identifiers and citation checks."""

from __future__ import annotations

import re

from pydantic import BaseModel


class EvidenceItem(BaseModel):
    id: str
    source: str
    version: str
    text: str


class CitationReport(BaseModel):
    cited: set[str]
    unknown_ids: set[str]
    uncited_claims_count: int | None = None


def cited_ids(text: str) -> set[str]:
    """Extract bracketed evidence markers such as ``[E1]``."""

    return set(re.findall(r"\[([A-Za-z][A-Za-z0-9_-]*)\]", text))


def check_citations(
    answer: str,
    evidence: list[EvidenceItem],
) -> CitationReport:
    """Report cited and unknown evidence IDs without judging semantic support."""

    cited = cited_ids(answer)
    known = {item.id for item in evidence}
    return CitationReport(cited=cited, unknown_ids=cited - known)
