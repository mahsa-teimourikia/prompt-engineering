from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
LAB_PATH = (
    ROOT
    / "curriculum"
    / "beginner"
    / "05-prompt-patterns-and-technique-selection"
    / "lab.py"
)


def load_lab():
    spec = importlib.util.spec_from_file_location("test_course05_lab", LAB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_selection_dataset_covers_system_and_prompt_choices():
    lab = load_lab()
    cases = lab.load_cases()

    assert len(cases) == 24
    assert {technique.name for technique in lab.TECHNIQUES} == {case.expected for case in cases}
    assert {"boundary", "safety", "deterministic", "cost", "injection"} <= {
        case.slice for case in cases
    }


def test_guardrails_reduce_unsafe_and_avoidable_choices():
    lab = load_lab()
    summary = {row["strategy"]: row for row in lab.compare_strategies()}

    assert summary["guardrailed"]["selection_accuracy"] > summary["pattern_match"]["selection_accuracy"]
    assert summary["guardrailed"]["unsafe_selection_rate"] == 0
    assert summary["pattern_match"]["unsafe_selection_rate"] > 0
    assert summary["maximalist"]["avoidable_complexity_rate"] > 0.8
    assert summary["guardrailed"]["mean_cost_units"] < summary["maximalist"]["mean_cost_units"]


def test_missing_authority_rejects_relevant_tool():
    lab = load_lab()
    case = next(case for case in lab.load_cases() if case.id == "TEC-015")

    assert lab.select("pattern_match", case) == "tool_calling"
    assert lab.select("guardrailed", case) == "no_model"


def test_provider_path_is_typed_and_offline_by_default(monkeypatch):
    lab = load_lab()
    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    result = lab.run_provider_case(lab.load_cases()[0])

    assert result.response.mode == "offline"
    assert isinstance(result.value, lab.SelectionResponse)
    assert result.value.technique == "direct_instruction"
