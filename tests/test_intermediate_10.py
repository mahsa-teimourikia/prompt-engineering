"""Tests for the Course 10 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/lab10.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab10", PATH)
assert SPEC and SPEC.loader
lab10 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab10)


def test_course_10_grounding_citations_and_abstention():
    results = lab10.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["unknown_citations"].numerator == 1
    assert results["abstention_when_no_evidence"].numerator == 1
    assert results["abstention_when_no_evidence"].denominator == 1
    assert results["claim_support_accuracy"].numerator == 2
    assert results["claim_support_accuracy"].denominator == 3
    assert results["retrieval_expectation_accuracy"].numerator == 3
    assert results["unauthorized_evidence_selected"].numerator == 0
    assert lab10.SEARCH_TOOL.name == "search_policies"


def test_course_10_filters_scope_before_ranking_and_handles_no_support():
    client = ReplayClient(PATH.parent / "fixtures/replays.json")
    visible = lab10.retrieve(
        client,
        "custom mug return policy",
        tenant="tenant-synthetic-a",
    )
    assert {item.id for item in visible} == {"POL-992"}
    assert lab10.retrieve(client, "price match competitors", tenant="tenant-synthetic-a") == []
    assert "POL-994" not in {item.id for item in visible}
