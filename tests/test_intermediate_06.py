"""Tests for the Course 06 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/06-reasoning-oriented-prompting/lab06.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab06", PATH)
assert SPEC and SPEC.loader
lab06 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab06
SPEC.loader.exec_module(lab06)


def test_course_06_metrics_and_risk_gate():
    client = ReplayClient(PATH.parent / "fixtures/replays.json")
    results = lab06.run_lab(client)
    assert results["root_cause_named"].numerator == 2
    assert results["recommended_action_exact"].numerator == 2
    assert results["routing_accuracy"].numerator == 2
    assert results["self_consistency"] == ("Increase DB connection pool ceiling", 2 / 3)
    assert lab06.classify_action_risk("DROP TABLE users") == "requires_approval"
    assert lab06.classify_action_risk("Rotate and compress logs") == "requires_approval"
    assert lab06.majority_vote(["a", "b"]) == ("no_consensus", 0.5)
    assert all(not client.generate(request).stale for request in lab06.build_requests())
