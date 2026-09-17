"""Tests for the Course 12 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/12-multimodal-prompt-engineering/lab12.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab12", PATH)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(lab12 := importlib.util.module_from_spec(SPEC))


def test_course_12_reconciliation_routes():
    results = lab12.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["routing_accuracy"].numerator == 4
    assert results["routing_accuracy"].denominator == 4
    extraction = lab12.InvoiceExtraction(
        invoice_id="INV-0007",
        total=500,
        is_contradictory=False,
        source_page=1,
        source_region="total_due",
        amount_confidence=0.98,
    )
    assert lab12.route(extraction, 800) == "human_review"
    assert lab12.route(extraction, 500) == "accepted_extraction"
    assert lab12.route(extraction.model_copy(update={"amount_confidence": 0.5}), 500) == "human_review"
    assert (PATH.parent / "fixtures/synthetic_invoice.png").exists()
