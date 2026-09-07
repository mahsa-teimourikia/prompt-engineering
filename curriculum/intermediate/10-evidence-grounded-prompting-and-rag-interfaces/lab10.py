"""Replay-backed retrieval, citation, and abstention experiments."""

from __future__ import annotations

import json
from pathlib import Path

from northstar.evidence import EvidenceItem, check_citations
from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest, ToolSpec


CASES = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())
POLICIES = json.loads((Path(__file__).parent / "fixtures/policies.json").read_text())
SEARCH_TOOL = ToolSpec(
    name="search_policies",
    description="Search approved policy documents for support evidence.",
    parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
)


def _reference_document(case: dict[str, object]) -> str:
    if case["id"] == "custom-mug":
        item = next(item for item in POLICIES if item["id"] == "POL-992")
        return (
            f"[Document ID: {item['id']}]\n"
            f"Title: {item['title']}\n"
            f"Content: {item['text']}"
        )
    if case["id"] == "unknown-citation":
        return "[Document ID: POL-404]\nContent: Custom mugs are available."
    return ""


def build_requests() -> list[PromptRequest]:
    requests: list[PromptRequest] = []
    for case in CASES:
        requests.extend(
            [
                PromptRequest(
                    case_id=f"i10/ungrounded/{case['id']}",
                    system="",
                    messages=[
                        Message(
                            role="user",
                            text=(
                                "You are a helpful customer support bot for Northstar.\n"
                                "Answer the following customer question:\n"
                                f"{case['question']}\n"
                            ),
                        )
                    ],
                ),
                PromptRequest(
                    case_id=f"i10/manual/{case['id']}",
                    system="",
                    messages=[
                        Message(
                            role="user",
                            text=(
                                "You are a strict customer support bot for Northstar.\n"
                                "You must answer the user's question using ONLY the provided Reference Document.\n"
                                "If the Reference Document does not contain the answer, you must output \"I don't know.\"\n"
                                "\n<reference_document>\n"
                                f"{_reference_document(case)}\n"
                                "</reference_document>\n\n"
                                f"User Question: {case['question']}\n"
                            ),
                        )
                    ],
                ),
                PromptRequest(
                    case_id=f"i10/tool/{case['id']}",
                    system="Use search_policies before answering and cite approved IDs.",
                    messages=[Message(role="user", text=case["question"])],
                    tools=[SEARCH_TOOL],
                ),
                PromptRequest(
                    case_id=f"i10/final/{case['id']}",
                    system="",
                    messages=[
                        Message(
                            role="user",
                            text=(
                                "You are a strict customer support bot for Northstar.\n"
                                "You must answer the user's question using ONLY the provided Reference Document.\n"
                                "If the Reference Document does not contain the answer, you must output \"I don't know.\"\n"
                                "\n<reference_document>\n"
                                f"{_reference_document(case)}\n"
                                "</reference_document>\n\n"
                                f"User Question: {case['question']}\n"
                            ),
                        )
                    ],
                ),
            ]
        )
    return requests


def retrieve(client: ModelClient, query: str, k: int = 2) -> list[EvidenceItem]:
    texts = [item["text"] for item in POLICIES]
    vectors = client.embed([query] + texts, case_id=f"i10/retrieve/{query}")
    query_vector = vectors[0]
    scored = []
    for item, vector in zip(POLICIES, vectors[1:]):
        score = sum(left * right for left, right in zip(query_vector, vector))
        scored.append((score, item))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    return [
        EvidenceItem(id=item["id"], source="course fixture", version=item["version"], text=item["text"])
        for _, item in scored[:k]
    ]


def is_abstention(text: str) -> bool:
    lowered = text.casefold()
    return "i don't know" in lowered or "insufficient evidence" in lowered


def run_lab(client: ModelClient) -> dict[str, Metric]:
    reports = []
    abstentions = 0
    for case in CASES:
        tool_request = next(item for item in build_requests() if item.case_id == f"i10/tool/{case['id']}")
        tool_response = client.generate(tool_request)
        query = tool_response.tool_calls[0].arguments.get("query", case["question"]) if tool_response.tool_calls else case["question"]
        evidence = retrieve(client, query)
        answer = client.generate(
            next(item for item in build_requests() if item.case_id == f"i10/final/{case['id']}")
        )
        report = check_citations(answer.text, evidence)
        reports.append(report)
        if case["expected_abstention"]:
            abstentions += int(is_abstention(answer.text))
    return {
        "unsupported_citations": rate(
            "unsupported_citations",
            sum(bool(report.unknown_ids) for report in reports),
            len(reports),
            "lower_is_better",
        ),
        "abstention_when_no_evidence": rate(
            "abstention_when_no_evidence",
            abstentions,
            sum(case["expected_abstention"] for case in CASES),
            "higher_is_better",
        ),
    }
