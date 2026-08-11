from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
LAB_PATH = (
    ROOT
    / "curriculum"
    / "beginner"
    / "03-constraints-examples-and-few-shot-learning"
    / "lab.py"
)


def load_lab():
    spec = importlib.util.spec_from_file_location("test_course03_lab", LAB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_dataset_has_frozen_train_and_held_out_slices():
    lab = load_lab()
    examples, cases = lab.load_dataset()

    assert len(examples) == 24
    assert len(cases) == 24
    assert set(lab.KEYWORDS) == {
        "access",
        "billing",
        "hardware",
        "network",
        "security",
        "software",
    }
    assert {"normal", "boundary", "urgent", "multilingual", "adversarial", "injection"} <= {
        case.slice for case in cases
    }


def test_selection_is_measured_and_poisoned_examples_regress_quality():
    lab = load_lab()
    summary = {row["strategy"]: row for row in lab.compare_strategies(count=4)}

    assert summary["diversity"]["macro_f1"] > summary["zero_shot"]["macro_f1"]
    assert summary["poisoned"]["accuracy"] < summary["zero_shot"]["accuracy"]
    assert summary["similarity"]["mean_example_tokens_estimated"] > 0
    assert summary["zero_shot"]["mean_example_tokens_estimated"] == 0


def test_more_examples_are_not_assumed_to_be_better():
    lab = load_lab()
    curve = lab.accuracy_by_example_count("similarity", maximum=8)
    best = max(curve, key=lambda row: (row["macro_f1"], row["accuracy"]))

    assert best["examples"] < curve[-1]["examples"]
    assert best["macro_f1"] > curve[-1]["macro_f1"]
    assert curve[0]["mean_example_tokens_estimated"] == 0
    assert curve[-1]["mean_example_tokens_estimated"] > curve[1]["mean_example_tokens_estimated"]


def test_provider_path_is_typed_and_offline_by_default(monkeypatch):
    lab = load_lab()
    _, cases = lab.load_dataset()
    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    result = lab.run_provider_case(cases[0])

    assert result.response.mode == "offline"
    assert isinstance(result.value, lab.RouteResponse)
    assert result.value.label in lab.KEYWORDS
