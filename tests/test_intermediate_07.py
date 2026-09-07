"""Tests for the Course 07 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/lab07.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab07", PATH)
assert SPEC and SPEC.loader
lab07 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab07
SPEC.loader.exec_module(lab07)


def test_course_07_workflow_and_constraints():
    results = lab07.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["policy_violations"].numerator == 0
    assert results["naive_policy_violations"].numerator == 1
    assert results["terminal_states"][-1] == "clarification_required"
    assert lab07.refund_eligible("ORD-8812") == "ineligible"
    assert lab07.refund_eligible("ORD-8813") == "eligible"
