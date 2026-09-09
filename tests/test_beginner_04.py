"""Tests for the Course 04 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient


ROOT = Path(__file__).parents[1]
LAB_PATH = ROOT / "curriculum/beginner/04-structured-outputs-and-typed-interfaces/lab04.py"
SPEC = importlib.util.spec_from_file_location("beginner_lab04", LAB_PATH)
assert SPEC and SPEC.loader
lab04 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab04
SPEC.loader.exec_module(lab04)


def test_course_04_schema_semantics_and_repair():
    client = ReplayClient(ROOT / "curriculum/beginner/04-structured-outputs-and-typed-interfaces/fixtures/replays.json")
    results = lab04.run_lab(client)
    assert results["syntax_valid"].numerator == 1
    assert results["unknown_evidence"].numerator == 1
    assert results["repair_attempts"] == 2
    assert results["repair_terminal"] == "valid"
    assert results["exhausted"] is None
    assert results["exhausted_terminal"] == "human_review"
    assert results["malformed_error"] == "not_json"
    assert all(not client.generate(request).stale for request in lab04.build_requests())
