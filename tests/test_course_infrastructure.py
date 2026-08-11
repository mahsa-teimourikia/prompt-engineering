from __future__ import annotations

import json
from datetime import date

import pytest

from prompt_course.datasets import Case, deterministic_split, load_jsonl, slice_counts
from prompt_course.evaluation import bootstrap_interval, evaluate_cases
from prompt_course.pricing import Pricing, estimate_cost
from prompt_course.providers import (
    DeterministicProvider,
    GenerationRequest,
    OpenAIProvider,
    ProviderUnavailableError,
    Usage,
    get_provider,
)
from prompt_course.token_usage import estimate_tokens, measure_components
from prompt_course.tracing import TraceCollector


def test_deterministic_provider_uses_same_contract_and_measures_runtime():
    provider = DeterministicProvider(lambda request: request.input.upper())
    response = provider.generate(GenerationRequest(input="claim 42", instructions="Classify"))

    assert response.text == "CLAIM 42"
    assert response.mode == "offline"
    assert response.elapsed_seconds >= 0
    assert response.usage.source == "estimated"
    assert response.usage.total_tokens == response.usage.input_tokens + response.usage.output_tokens


def test_deterministic_provider_validates_structured_fixture():
    from pydantic import BaseModel

    class Answer(BaseModel):
        label: str

    provider = DeterministicProvider(lambda request: '{"label":"refund"}')
    result = provider.generate_structured(GenerationRequest(input="claim 42"), Answer)

    assert result.value.label == "refund"
    assert result.response.mode == "offline"


def test_factory_never_uses_live_provider_implicitly(monkeypatch):
    monkeypatch.delenv("PROMPT_COURSE_PROVIDER", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "not-used")
    assert isinstance(get_provider(), DeterministicProvider)


def test_openai_adapter_fails_safely_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider()
    assert not provider.available
    with pytest.raises(ProviderUnavailableError, match="OPENAI_API_KEY"):
        provider.generate(GenerationRequest(input="test"))


def test_dataset_helpers_are_stable_and_report_slices(tmp_path):
    rows = [
        {"id": "a", "input": "clear", "expected": "ok", "slice": "normal"},
        {"id": "b", "input": "ambiguous", "expected": "clarify", "slice": "ambiguous"},
    ]
    path = tmp_path / "cases.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    cases = load_jsonl(path)
    assert deterministic_split("stable-id") == deterministic_split("stable-id")
    assert slice_counts(cases) == {"ambiguous": 1, "normal": 1}


def test_evaluation_reports_overall_slices_and_bootstrap_interval():
    cases = [
        Case("1", "clear", "answer", "normal"),
        Case("2", "missing", "clarify", "missing"),
        Case("3", "clear again", "answer", "normal"),
    ]
    summary = evaluate_cases(
        cases,
        system=lambda case: "clarify" if "missing" in case.input else "answer",
        grader=lambda output, case: {"correct": output == case.expected},
    )

    assert summary.overall == {"correct": 1.0}
    assert summary.by_slice["missing"] == {"correct": 1.0}
    assert bootstrap_interval([0, 1, 1], samples=200, seed=4) == bootstrap_interval(
        [0, 1, 1], samples=200, seed=4
    )


def test_usage_cost_and_component_measurement_keep_provenance():
    usage = Usage(1_000, 500, 1_500, "provider")
    pricing = Pricing(2.0, 8.0, "https://example.com/pricing", date(2026, 8, 11))
    cost = estimate_cost(usage, pricing)

    assert cost.amount == pytest.approx(0.006)
    assert cost.usage_source == "provider"
    assert estimate_tokens("one two") > 0
    assert [item.component for item in measure_components({"instructions": "Do X", "input": "Y"})] == [
        "instructions",
        "input",
    ]


def test_trace_collector_exposes_structured_events_not_private_reasoning():
    trace = TraceCollector()
    event = trace.record("retrieve", "retrieval", "Selected current policy", source_id="policy-7")

    assert event.sequence == 1
    assert event.elapsed_seconds >= 0
    assert trace.as_dicts()[0]["attributes"] == {"source_id": "policy-7"}
