from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
LAB_PATH = (
    ROOT
    / "curriculum"
    / "beginner"
    / "04-structured-outputs-and-typed-interfaces"
    / "lab.py"
)


def load_lab():
    spec = importlib.util.spec_from_file_location("test_course04_lab", LAB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_structured_output_experiment_uses_twenty_sliced_cases():
    lab = load_lab()
    cases = lab.load_cases()

    assert len(cases) == 20
    assert {"normal", "missing_information", "injection", "conflicting_evidence"} <= {
        case.slice for case in cases
    }


def test_typed_and_semantic_validation_prevent_unsafe_acceptance():
    lab = load_lab()
    results = lab.run_experiment()
    summary = {row["strategy"]: row for row in lab.summarize(results)}

    assert summary["free_text"]["parse_success"] == 0.0
    assert summary["json_prompt"]["safe_decision"] < 1.0
    assert summary["pydantic_validation"]["safe_decision"] == 1.0
    assert summary["provider_native"]["schema_valid"] == 1.0
    assert summary["provider_native"]["semantic_correct"] < 1.0


def test_repair_is_bounded_to_unknown_root_fields():
    lab = load_lab()
    extra_case = next(case for case in lab.load_cases() if int(case.id.split("-")[-1]) % 5 == 1)
    raw = lab.candidate_for(extra_case, "json_prompt")

    repaired = lab.bounded_repair(raw)
    assert repaired is not None
    assert lab.evaluate_candidate(extra_case, "pydantic_validation", repaired).semantic_correct

    malformed_case = next(case for case in lab.load_cases() if int(case.id.split("-")[-1]) % 5 == 0)
    assert lab.bounded_repair(lab.candidate_for(malformed_case, "json_prompt")) is None


def test_provider_path_is_offline_by_default(monkeypatch):
    lab = load_lab()
    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    result = lab.run_provider_case(lab.load_cases()[0])

    assert result.response.mode == "offline"
    assert result.value.case_id == "CLM-1001"
