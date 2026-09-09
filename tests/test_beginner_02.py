"""Tests for the Course 02 offline lab."""

import importlib.util
import sys
import warnings
from pathlib import Path

from northstar.runtime import ReplayClient


ROOT = Path(__file__).parents[1]
LAB_PATH = ROOT / "curriculum/beginner/02-instruction-contracts/lab02.py"
SPEC = importlib.util.spec_from_file_location("beginner_lab02", LAB_PATH)
assert SPEC and SPEC.loader
lab02 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab02
SPEC.loader.exec_module(lab02)


def test_course_02_gate_and_contract_metrics():
    client = ReplayClient(ROOT / "curriculum/beginner/02-instruction-contracts/fixtures/replays.json")
    results = lab02.run_lab(client)
    assert results["safe_normal_draft"].numerator == 1
    assert results["evidence_cited"].numerator == 1
    assert results["forbidden_phrase_violations"].numerator == 0
    assert results["actions"][3] == "human_review"
    assert all(not client.generate(request).stale for request in lab02.build_requests())


def test_course_02_version_change_is_stale():
    request = lab02.build_requests()[0]
    client = ReplayClient(ROOT / "curriculum/beginner/02-instruction-contracts/fixtures/replays.json")
    changed = request.model_copy(update={"system": request.system.replace("v3", "v4")})
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        assert client.generate(changed).stale
    assert len(captured) == 1
