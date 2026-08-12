from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
LAB_PATH = (
    ROOT
    / "curriculum"
    / "intermediate"
    / "06-reasoning-oriented-prompting"
    / "lab.py"
)


def load_lab():
    spec = importlib.util.spec_from_file_location("test_course06_lab", LAB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_incident_dataset_has_twenty_four_reasoning_slices():
    lab = load_lab()
    cases = lab.load_cases()

    assert len(cases) == 24
    assert set(lab.Action.__args__) == {case.expected for case in cases}
    assert {"missing_evidence", "conflicting", "injection", "deterministic", "recovered"} <= {
        case.slice for case in cases
    }


def test_verification_and_adaptive_routing_improve_supported_decisions():
    lab = load_lab()
    summary = {row["strategy"]: row for row in lab.compare_strategies()}

    assert summary["planner_verifier"]["decision_accuracy"] > summary["direct"]["decision_accuracy"]
    assert summary["planner_verifier"]["supported_decision_rate"] == 1
    assert summary["planner_verifier"]["safe_escalation_accuracy"] == 1
    assert summary["adaptive"]["decision_accuracy"] == summary["planner_verifier"]["decision_accuracy"]
    assert summary["adaptive"]["mean_calls"] < summary["planner_verifier"]["mean_calls"]


def test_more_samples_do_not_verify_a_shared_false_premise():
    lab = load_lab()
    case = next(case for case in lab.load_cases() if case.id == "RSN-019")
    voted, candidates, calls = lab.decide(case, "self_consistency")
    verified, _, verified_calls = lab.decide(case, "planner_verifier")

    assert voted.action == "rotate_credentials"
    assert candidates.count("rotate_credentials") > candidates.count("collect_evidence")
    assert calls == 5
    assert verified.action == "collect_evidence"
    assert verified_calls == 2


def test_artifact_is_typed_and_provider_defaults_offline(monkeypatch):
    lab = load_lab()
    fields = set(lab.DecisionArtifact.model_fields)
    assert fields == {"action", "evidence_ids", "checks", "assumptions", "needs_human"}

    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    result = lab.run_provider_case(lab.load_cases()[0])
    assert result.response.mode == "offline"
    assert isinstance(result.value, lab.DecisionArtifact)
    assert result.value.action == "rollback"
