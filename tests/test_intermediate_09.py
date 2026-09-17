"""Tests for the Course 09 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/09-conversation-and-long-context-engineering/lab09.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab09", PATH)
assert SPEC and SPEC.loader
lab09 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab09
SPEC.loader.exec_module(lab09)


def test_course_09_retention_and_conflict():
    results = lab09.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["window_order_id_accuracy"].numerator == 0
    assert results["summary_order_id_accuracy"].numerator == 2
    assert results["state_order_id_accuracy"].numerator == 2
    assert results["state_candidates_authorized"] is True
    merged = lab09.merge_state(
        lab09.UserState(active_order_id="ORD-5592"),
        lab09.UserState(active_order_id="ORD-7710"),
    )
    assert merged.needs_confirmation is True
    assert merged.active_order_id == "ORD-5592"
    assert merged.proposed_order_id == "ORD-7710"


def test_course_09_model_state_is_only_a_candidate():
    candidate = lab09.UserState(active_order_id="ORD-OTHER-TENANT")
    assert lab09.state_candidate_is_authorized(candidate, {"ORD-5592"}) is False
