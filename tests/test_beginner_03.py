"""Tests for the Course 03 offline lab."""

import importlib.util
import sys
from pathlib import Path

from northstar.runtime import ReplayClient


ROOT = Path(__file__).parents[1]
LAB_PATH = ROOT / "curriculum/beginner/03-constraints-examples-and-few-shot-learning/lab03.py"
SPEC = importlib.util.spec_from_file_location("beginner_lab03", LAB_PATH)
assert SPEC and SPEC.loader
lab03 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab03
SPEC.loader.exec_module(lab03)


def test_course_03_recorded_strategy_ordering():
    client = ReplayClient(ROOT / "curriculum/beginner/03-constraints-examples-and-few-shot-learning/fixtures/replays.json")
    metrics = lab03.run_lab(client)
    assert metrics["zero_accuracy"].numerator == 3
    assert metrics["static_accuracy"].numerator == 4
    assert metrics["similarity_accuracy"].numerator == 5
    assert all(not client.generate(request).stale for request in lab03.build_requests())


def test_course_03_selection_prevents_query_leakage():
    query = lab03.EXAMPLE_BANK[0]["message"]
    selected = lab03.select_examples(2, query, lab03.EXAMPLE_BANK, "b03/test/leakage")
    assert query not in {example["message"] for example in selected}
