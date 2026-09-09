"""Tests for the Course 01 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
LAB_PATH = ROOT / "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/lab01.py"
SPEC = importlib.util.spec_from_file_location("beginner_lab01", LAB_PATH)
assert SPEC and SPEC.loader
lab01 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab01
SPEC.loader.exec_module(lab01)


def test_course_01_replay_lab_metrics_and_requests():
    replay = ROOT / "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/fixtures/replays.json"
    client = ReplayClient(replay)
    results = lab01.run_lab(client)
    assert results["baseline_accuracy"].numerator == 4
    assert results["baseline_accuracy"].denominator == 4
    assert results["middle_accuracy"].numerator == 3
    assert results["temperature_comparison"] == ("unknown", "refund")
    assert results["weak_missing_evidence"].numerator == 1
    assert results["abstention_missing_evidence"].numerator == 1
    assert all(not client.generate(request).stale for request in lab01.build_requests())


def test_course_01_schema_rejects_unknown_category():
    from pydantic import ValidationError

    try:
        lab01.SupportClassification(category="payment")
    except ValidationError:
        return
    raise AssertionError("unsupported category was accepted")
