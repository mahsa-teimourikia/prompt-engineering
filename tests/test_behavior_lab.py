from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
LAB_PATH = (
    ROOT
    / "curriculum"
    / "beginner"
    / "01-llm-behavior-and-prompt-anatomy"
    / "lab.py"
)


def load_lab():
    spec = importlib.util.spec_from_file_location("test_course01_lab", LAB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_behavior_dataset_has_twenty_sliced_cases():
    lab = load_lab()
    cases = lab.load_cases()

    assert len(cases) == 20
    assert {"refund", "shipping", "account", "unknown"} == {case.expected for case in cases}
    assert {"normal", "ambiguous", "boundary", "missing_evidence", "multilingual", "injection"} <= {
        case.slice for case in cases
    }


def test_controlled_packet_changes_are_measurable():
    lab = load_lab()
    summary = {row["strategy"]: row for row in lab.compare_strategies(repeats=5)}

    assert summary["stable"]["accuracy"] > summary["vague"]["accuracy"]
    assert summary["stable"]["instability_rate"] == 0
    assert summary["high_variation"]["instability_rate"] > 0
    assert summary["evidence_middle"]["accuracy"] < summary["stable"]["accuracy"]
    assert summary["overloaded"]["mean_packet_tokens_estimated"] > 800
    assert summary["overloaded"]["accuracy"] < summary["stable"]["accuracy"]


def test_missing_evidence_has_a_safe_outcome():
    lab = load_lab()
    missing = next(case for case in lab.load_cases() if case.slice == "missing_evidence")
    packet = lab.packet_for(missing, "stable")

    assert not packet.evidence_available
    assert lab.classify(packet) == "unknown"
    assert lab.metrics(lab.run_strategy("stable"))["unsupported_rate"] == 0


def test_provider_path_is_typed_and_offline_by_default(monkeypatch):
    lab = load_lab()
    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    result = lab.run_provider_case(lab.load_cases()[0])

    assert result.response.mode == "offline"
    assert isinstance(result.value, lab.ClassificationResponse)
    assert result.value.label == "refund"
