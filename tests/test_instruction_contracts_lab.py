from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
LAB_PATH = ROOT / "curriculum" / "beginner" / "02-instruction-contracts" / "lab.py"


def load_lab():
    spec = importlib.util.spec_from_file_location("test_course02_lab", LAB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_contract_experiment_uses_twenty_sliced_cases_and_seven_versions():
    lab = load_lab()
    cases = lab.load_cases()

    assert len(cases) == 20
    assert len(lab.VERSIONS) == 7
    assert {"clear", "missing_evidence", "conflicting_evidence", "out_of_scope", "injection"} <= {
        case.slice for case in cases
    }


def test_contract_components_produce_measurable_improvement():
    lab = load_lab()
    summary = {row["version"]: row for row in lab.summarize(lab.run_experiment())}

    assert summary["v0"]["task_correctness"] < summary["v6"]["task_correctness"]
    assert summary["v0"]["unsupported_claim_rate"] > 0
    assert summary["v6"]["unsupported_claim_rate"] == 0
    assert summary["v6"]["clarification_correctness"] == 1
    assert summary["v6"]["schema_validity"] == 1
    assert summary["v6"]["prompt_tokens_estimated"] > summary["v0"]["prompt_tokens_estimated"]


def test_injection_is_rejected_and_provider_defaults_offline(monkeypatch):
    lab = load_lab()
    attack = next(case for case in lab.load_cases() if case.slice == "injection")
    result = lab.evaluate_version(lab.CONTRACT, attack)

    assert result.outcome == "reject"
    assert result.schema_valid

    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    provider_result = lab.run_provider_case(lab.load_cases()[0])
    assert provider_result.response.mode == "offline"
    assert provider_result.value.outcome == "draft"
