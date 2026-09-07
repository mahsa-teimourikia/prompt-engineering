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
    assert results["contradictions_routed"].numerator == 2
    assert lab12.route(lab12.InvoiceExtraction(invoice_id="INV-0007", total=500, is_contradictory=False), 800) == "human_review"
    assert (PATH.parent / "fixtures/synthetic_invoice.png").exists()
