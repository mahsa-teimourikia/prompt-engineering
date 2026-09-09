"""Tests for the Course 05 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient


ROOT = Path(__file__).parents[1]
LAB_PATH = ROOT / "curriculum/beginner/05-prompt-patterns-and-technique-selection/lab05.py"
SPEC = importlib.util.spec_from_file_location("beginner_lab05", LAB_PATH)
assert SPEC and SPEC.loader
lab05 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab05
SPEC.loader.exec_module(lab05)


def test_course_05_technique_metrics_and_validator():
    client = ReplayClient(ROOT / "curriculum/beginner/05-prompt-patterns-and-technique-selection/fixtures/replays.json")
    results = lab05.run_lab(client)
    assert results["zero_accuracy"].numerator == 1
    assert results["system_accuracy"].numerator == 2
    assert results["few_accuracy"].numerator == 4
    assert results["regex_zero_tokens_accuracy"].numerator == 3
    assert "direct instruction" in results["worksheet"]
    assert all(not client.generate(request).stale for request in lab05.build_requests())


def test_course_05_validation_is_exact():
    assert lab05.validate_code("PRD-1234") == "PRD-1234"
    assert lab05.validate_code("The code is PRD-1234") is None
    assert lab05.validate_code("prd 1234") is None
