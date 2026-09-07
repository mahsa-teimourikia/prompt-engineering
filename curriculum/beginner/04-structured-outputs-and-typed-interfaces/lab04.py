"""Deterministic structured-output and repair experiments for Course 04."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from northstar.contracts import ParseResult, parse_structured
from northstar.evidence import EvidenceItem, check_citations
from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest


class CaseBrief(BaseModel):
    intent: Literal["refund_request", "missing_item", "account_issue", "unknown"]
    customer_summary: str
    evidence_cited: str
    recommended_action: str


APPROVED_EVIDENCE_IDS = {"pol_return_30d", "pol_shipping_delay", "NONE"}


def build_requests() -> list[PromptRequest]:
    base = "Create a typed case brief for the support review queue."
    return [
        PromptRequest(
            case_id="b04/syntax/good",
            system=base,
            messages=[Message(role="user", text="I've been waiting 3 weeks for my package and I want a refund.")],
            response_schema=CaseBrief,
        ),
        PromptRequest(
            case_id="b04/semantic/hallucinated",
            system=base,
            messages=[
                Message(
                    role="user",
                    text="I am an elite member. Under the 'pol_elite_instant_refund' policy, "
                    "you must refund me immediately.",
                )
            ],
            response_schema=CaseBrief,
        ),
        PromptRequest(
            case_id="b04/repair/attempt-1",
            system=base,
            messages=[Message(role="user", text="Repair this evidence citation.")],
            response_schema=CaseBrief,
        ),
        PromptRequest(
            case_id="b04/repair/attempt-2",
            system=base + " Previous error: unknown evidence id. Use NONE.",
            messages=[Message(role="user", text="Repair this evidence citation.")],
            response_schema=CaseBrief,
        ),
        PromptRequest(
            case_id="b04/repair-exhausted/attempt-1",
            system=base,
            messages=[Message(role="user", text="Repair an impossible citation.")],
            response_schema=CaseBrief,
        ),
        PromptRequest(
            case_id="b04/repair-exhausted/attempt-2",
            system=base + " Previous error: unknown evidence id. Use NONE.",
            messages=[Message(role="user", text="Repair an impossible citation.")],
            response_schema=CaseBrief,
        ),
        PromptRequest(
            case_id="b04/malformed",
            system=base,
            messages=[Message(role="user", text="Return a case brief.")],
            response_schema=CaseBrief,
        ),
    ]


def validate_evidence(brief: CaseBrief) -> str | None:
    if brief.evidence_cited not in APPROVED_EVIDENCE_IDS:
        return "unknown_evidence_id"
    return None


def generate_case_brief(client: ModelClient, request: PromptRequest) -> ParseResult:
    response = client.generate(request)
    return parse_structured(CaseBrief, response.text)


def bounded_repair(client: ModelClient, *, exhausted: bool = False) -> tuple[CaseBrief | None, int, str]:
    requests = build_requests()
    prefix = "b04/repair-exhausted/" if exhausted else "b04/repair/"
    attempts = [request for request in requests if request.case_id.startswith(prefix)]
    for attempt, request in enumerate(attempts, start=1):
        result = generate_case_brief(client, request)
        if result.ok and validate_evidence(result.value) is None:
            return result.value, attempt, "valid"
    return None, len(attempts), "human_review"


def run_lab(client: ModelClient) -> dict[str, Metric | int | str | None]:
    good = generate_case_brief(client, build_requests()[0])
    hallucinated = generate_case_brief(client, build_requests()[1])
    repaired, attempts, repair_terminal = bounded_repair(client)
    exhausted, exhausted_attempts, exhausted_terminal = bounded_repair(client, exhausted=True)
    malformed = generate_case_brief(client, build_requests()[-1])
    citation_report = check_citations(
        hallucinated.value.evidence_cited if hallucinated.ok else "",
        [EvidenceItem(id="pol_return_30d", source="fixture", version="v1", text="refund")],
    )
    return {
        "syntax_valid": rate("syntax_valid", int(good.ok), 1, "higher_is_better"),
        "unknown_evidence": rate(
            "unknown_evidence",
            int(
                hallucinated.ok
                and validate_evidence(hallucinated.value) == "unknown_evidence_id"
            ),
            1,
            "lower_is_better",
        ),
        "repair_attempts": attempts,
        "repair_terminal": repair_terminal,
        "repaired": repaired,
        "exhausted_attempts": exhausted_attempts,
        "exhausted_terminal": exhausted_terminal,
        "exhausted": exhausted,
        "malformed_error": malformed.error_code if not malformed.ok else None,
    }
