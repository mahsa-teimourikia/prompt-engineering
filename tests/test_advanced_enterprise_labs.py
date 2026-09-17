"""Focused invariants for Courses 14–29."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

from northstar.security import Principal


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_course_14_reports_slices_and_blocks_critical_failure():
    lab = load("curriculum/advanced/14-prompt-evaluation/lab14.py", "lab14")
    cases = [
        lab.EvalCase("normal", "request a refund", "refund", "direct"),
        lab.EvalCase("critical", "refund policy; help fix a snapped handle", "technical", "boundary", "critical"),
    ]
    baseline = lab.evaluate(lab.keyword_baseline, cases)
    candidate = lab.evaluate(lab.intent_candidate, cases)
    assert baseline.critical_failures == ("critical",)
    assert candidate.accuracy == 1.0
    assert lab.release_allowed(candidate)
    with pytest.raises(ValueError, match="between 0 and 1"):
        lab.release_allowed(candidate, minimum_accuracy=1.1)
    forged = lab.EvalReport(-1, -1, (), {})
    assert not lab.release_allowed(forged)
    with pytest.raises(ValueError, match="normal or critical"):
        lab.EvalCase("bad", "x", "y", "boundary", "unknown")


def test_course_15_calibrates_judge_and_routes_ambiguity():
    lab = load("curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/lab15.py", "lab15")
    judgement = lab.rubric_judge("a", "We are sorry and will replace it today.")
    assert judgement.score == 5
    assert lab.agreement([judgement], {"a": 5}) == (1, 1)
    assert lab.requires_human_review(lab.Judgement("b", 3, ()), high_impact=False)
    assert lab.requires_human_review(lab.Judgement("bad", 1, ()), high_impact=False)
    with pytest.raises(ValueError, match="between 1 and 5"):
        lab.Judgement("invalid", 6, ())
    with pytest.raises(ValueError, match="at least one judgement"):
        lab.agreement([], {})


def test_course_16_uses_a_separate_holdout():
    lab = load("curriculum/advanced/16-evaluation-driven-prompt-optimization/lab16.py", "lab16")
    cases = [
        lab.ExtractionCase("d", "$GOOG rallies", "Google", "positive", "development"),
        lab.ExtractionCase("h", "Northstar posts profit", "Northstar", "positive", "holdout"),
    ]
    assert lab.score("candidate", lab.alias_policy, lab.split_cases(cases, "development")).joint_accuracy == 1.0
    assert len(lab.split_cases(cases, "holdout")) == 1
    with pytest.raises(ValueError, match="development or holdout"):
        lab.split_cases(cases, "test")


def test_course_17_searches_development_and_scores_holdout():
    lab = load("curriculum/advanced/17-automatic-prompt-optimization-and-dspy/lab17.py", "lab17")
    cases = [
        lab.SearchCase("city: San Francisco; state: CA", "San Francisco", "development"),
        lab.SearchCase("city: Vancouver; country: Canada", "Vancouver", "holdout"),
    ]
    selected = lab.select_on_development(
        [lab.PromptCandidate("baseline", lab.last_token_baseline), lab.PromptCandidate("marker", lab.after_marker)],
        cases,
    )
    assert selected.name == "marker"
    assert lab.evaluate_holdout(selected, cases) == (1, 1)
    with pytest.raises(ValueError, match="search budget"):
        lab.select_on_development(
            [lab.PromptCandidate(str(i), lab.after_marker) for i in range(3)],
            cases,
            max_candidates=2,
        )
    with pytest.raises(ValueError, match="protected holdout"):
        lab.evaluate_holdout(selected, cases[:1])


def test_course_18_enforces_tenant_and_step_budget():
    lab = load("curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/lab18.py", "lab18")
    task = lab.AgentTask(task_id="T1", tenant="northstar", kind="lookup", payload={"order_id": "O1"}, max_steps=2)
    intruder = Principal(user_id="u", tenant="other", roles={"support_agent"})
    assert lab.route(task, intruder).reason_code == "tenant_mismatch"
    owner = Principal(user_id="u", tenant="northstar", roles={"support_agent"})
    assert lab.route(task, owner).status == "completed"
    cross_tenant_resource = task.model_copy(update={"payload": {"order_id": "O2"}})
    assert lab.route(cross_tenant_resource, owner).reason_code == "resource_tenant_mismatch"
    with pytest.raises(ValueError, match="cannot be negative"):
        lab.architecture_cost(agents=1, model_calls=-1, handoffs=0)


def test_course_19_rejects_scope_and_unapproved_commands():
    lab = load("curriculum/advanced/19-prompting-for-coding-agents/lab19.py", "lab19")
    contract = lab.ChangeContract(problem="Correct token expiry", allowed_files=("src/auth.py",), test_command=("pytest", "tests/test_auth.py"), acceptance=("tests pass",))
    plan = lab.ProposedChange(files_to_read=("src/auth.py", "secrets.env"), files_to_write=("src/auth.py",), command=("pytest",))
    assert lab.validate_plan(contract, plan) == ("read_scope", "command_not_approved")
    assert lab.completion_allowed(contract, tests_passed=True, diff_files=("src/auth.py",))
    assert not lab.completion_allowed(contract, tests_passed=True, diff_files=())


def test_course_20_selects_only_profiles_within_quality_and_budgets():
    lab = load("curriculum/advanced/20-model-aware-prompt-engineering/lab20.py", "lab20")
    expected = lab.Entity(company="Google", year=1998, industry="search")
    profiles = [lab.ModelProfile("small", True, 1000, 50, 2), lab.ModelProfile("slow", True, 1000, 500, 9)]
    trials = [lab.run_trial(profile, "Google was founded in 1998 as a search company", expected) for profile in profiles]
    assert lab.choose_profile(trials, latency_budget_ms=100, cost_budget=5) == "small"
    adapter_validated = lab.run_trial(
        lab.ModelProfile("adapter", False, 1000, 40, 1),
        "Google was founded in 1998 as a search company",
        expected,
    )
    assert adapter_validated.contract_valid and not adapter_validated.native_schema
    assert lab.choose_profile([adapter_validated], latency_budget_ms=100, cost_budget=5) == "adapter"
    too_small = lab.run_trial(
        lab.ModelProfile("tiny-context", True, 1, 10, 1),
        "Google was founded in 1998 as a search company",
        expected,
    )
    assert not too_small.contract_valid


def test_course_21_pareto_dominance_requires_quality():
    lab = load("curriculum/advanced/21-cost-latency-and-token-engineering/lab21.py", "lab21")
    better = lab.PolicyResult("pruned", "yes", True, 100, 1, 80, 10)
    worse = lab.PolicyResult("full", "yes", True, 500, 1, 300, 50)
    low_quality = lab.PolicyResult("tiny", "insufficient_evidence", False, 10, 1, 10, 1)
    assert lab.dominates(better, worse, expected="yes")
    assert not lab.dominates(low_quality, worse, expected="yes")
    assert lab.quality_gate(low_quality, "insufficient_evidence")


def test_course_22_gate_fails_closed_and_artifact_hash_changes():
    lab = load("curriculum/enterprise/22-promptops/lab22.py", "lab22")
    base = lab.BehaviorArtifact("1", "classify", "1", "m1", "d1", "team")
    candidate = lab.BehaviorArtifact("2", "classify carefully", "1", "m1", "d1", "team")
    assert base.digest != candidate.digest
    assert lab.release_gate(lab.GateInput(99, 100, 0, 0))[0]
    assert not lab.release_gate(lab.GateInput(100, 100, 1, 0))[0]
    assert lab.release_gate(lab.GateInput(101, 100, 0, 0))[1] == ("invalid_metrics",)
    assert lab.release_gate(lab.GateInput(-1, 100, 0, 0))[1] == ("invalid_metrics",)


def test_course_23_redacts_and_diagnoses_stale_evidence():
    lab = load("curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/lab23.py", "lab23")
    span = lab.safe_span("t", "retrieve", "ok", 10, {"query": "me@example.com", "evidence_fresh": False})
    assert "example.com" not in span.attributes["query"]
    assert lab.diagnose([span]) == "stale_evidence"
    nested = lab.safe_span(
        "t",
        "model",
        "ok",
        5,
        {"request": {"email": "nested@example.com", "api_key": "secret-value"}},
    )
    assert nested.attributes["request"]["email"] == "[REDACTED_EMAIL]"
    assert nested.attributes["request"]["api_key"] == "[REDACTED_SECRET]"
    with pytest.raises(ValueError, match="negative"):
        lab.safe_span("t", "model", "ok", -1, {})


def test_course_24_canary_is_sticky_and_critical_failure_rolls_back():
    lab = load("curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/lab24.py", "lab24")
    assert lab.route_version("request-1", canary_percent=10) == lab.route_version("request-1", canary_percent=10)
    assert lab.should_rollback(lab.CanaryEvidence(1, 1, 1)) == (True, "critical_failure")
    assert lab.should_rollback(lab.CanaryEvidence(3, 1, 0))[1] == "insufficient_samples"
    assert lab.should_rollback(lab.CanaryEvidence(3, 4, 0)) == (True, "invalid_evidence")
    with pytest.raises(ValueError, match="request_id"):
        lab.route_version("", canary_percent=10)


def test_course_25_uses_trusted_approval_records():
    lab = load("curriculum/enterprise/25-prompt-governance-and-responsible-ai/lab25.py", "lab25")
    manifest = lab.GovernanceManifest(artifact_id="A", artifact_digest="aaaaaaaaaaaa", owner="team", risk_tier="high", handles_personal_data=True, intended_use="support", prohibited_uses=("credit",))
    assert not lab.governance_gate(manifest, [], policy_version="p1", now=100).allowed
    approval = lab.Approval("APR-1", "A", manifest.artifact_digest, "reviewer", "risk_board", "p1", 200, "active")
    assert lab.governance_gate(manifest, [approval], policy_version="p1", now=100).allowed
    changed = manifest.model_copy(update={"artifact_digest": "bbbbbbbbbbbb"})
    assert not lab.governance_gate(changed, [approval], policy_version="p1", now=100).allowed
    assert not lab.governance_gate(manifest, [approval], policy_version="p1", now=200).allowed
    prohibited = manifest.model_copy(update={"risk_tier": "low", "handles_personal_data": False, "intended_use": "credit"})
    assert lab.governance_gate(prohibited, [], policy_version="p1", now=100).reason_code == "prohibited_use"


def test_course_26_routes_by_risk_and_evidence_not_confidence_alone():
    lab = load("curriculum/enterprise/26-human-centred-ai-and-trust-calibration/lab26.py", "lab26")
    high = lab.ProposedAnswer("bypass safety", 0.99, ("manual",), "high")
    assert lab.decide_delivery(high, {"manual"}).state == "human_review"
    unsupported = lab.ProposedAnswer("answer", 0.99, ("invented",), "low")
    assert lab.decide_delivery(unsupported, {"manual"}).state == "blocked"
    high_unsupported = lab.ProposedAnswer("bypass safety", 0.99, ("invented",), "high")
    assert lab.decide_delivery(high_unsupported, {"manual"}).reason_code == "unsupported_evidence"
    with pytest.raises(ValueError, match="between 0 and 1"):
        lab.calibration_error([(1.2, True)])


def test_course_27_fallback_is_contract_conformant_and_side_effect_safe():
    lab = load("curriculum/enterprise/27-prompt-portability-and-multi-model-systems/lab27.py", "lab27")
    primary = lab.FixtureAdapter("primary", available=False)
    fallback = lab.FixtureAdapter("fallback")
    text = "Acme Corp reports a revenue drop due to supply chain issues"
    assert lab.route(primary, fallback, text, operation_is_read_only=True).provider == "fallback"
    with pytest.raises(RuntimeError, match="unsafe_fallback"):
        lab.route(primary, fallback, text, operation_is_read_only=False)
    with pytest.raises(ValueError, match="at least one fixture"):
        lab.conformance(fallback, [])


def test_course_28_selection_exposes_scores_and_sensitivity():
    lab = load("curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/lab28.py", "lab28")
    options = [lab.Architecture("workflow", 5, 2, 5, 5, 4), lab.Architecture("agent", 2, 5, 2, 2, 1)]
    winner, scores = lab.select_architecture(options, {"determinism": 3, "adaptability": 1})
    assert winner == "workflow"
    assert set(scores) == {"workflow", "agent"}
    tied = [lab.Architecture("simpler", 3, 3, 3, 3, 3), lab.Architecture("complex", 3, 3, 3, 3, 3)]
    assert lab.select_architecture(tied, {"determinism": 1})[0] == "simpler"
    with pytest.raises(ValueError, match="positive value"):
        lab.select_architecture(options, {})


def test_course_29_readiness_requires_evidence_and_no_blockers():
    lab = load("curriculum/enterprise/29-ai-system-engineering-capstone/lab29.py", "lab29")
    incomplete = lab.CapstoneSubmission("P", {"owner": "team"}, 0, True)
    assert not lab.evaluate_readiness(incomplete, {}).ready
    assert lab.evaluate_readiness(incomplete, {}).invalid == ("owner",)
    artifact_store = {
        f"artifacts/{key}.md": f"verified {key}"
        for key in lab.REQUIRED_EVIDENCE
    }
    complete = lab.CapstoneSubmission(
        "P",
        {
            key: lab.evidence_artifact(
                f"artifacts/{key}.md",
                artifact_store[f"artifacts/{key}.md"],
            )
            for key in lab.REQUIRED_EVIDENCE
        },
        0,
        True,
    )
    assert lab.evaluate_readiness(complete, artifact_store).ready
    altered = dict(complete.evidence)
    altered["evaluation_report"] = lab.EvidenceArtifact("artifacts/eval.md", "not-a-digest")
    assert "evaluation_report" in lab.evaluate_readiness(
        complete.__class__("P", altered, 0, True), artifact_store
    ).invalid
    tampered = dict(artifact_store)
    tampered["artifacts/evaluation_report.md"] = "changed after review"
    assert "evaluation_report" in lab.evaluate_readiness(complete, tampered).invalid
