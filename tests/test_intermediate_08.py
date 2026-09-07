"""Tests for the Course 08 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/08-context-engineering/lab08.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab08", PATH)
assert SPEC and SPEC.loader
lab08 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab08
SPEC.loader.exec_module(lab08)


def test_course_08_policy_boundary_and_budget():
    results = lab08.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["approved_cases"].numerator == 1
    assert results["injection_score"] >= 0.8
    assert results["policy_retained"] is True
    assert results["chat_history_dropped"] is True
    assert lab08.policy_allows(20) is False
