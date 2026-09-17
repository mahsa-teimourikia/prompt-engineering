"""Rebuild Courses 14–29 as deterministic, credential-free guided labs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

import nbformat


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Course:
    path: str
    number: int
    title: str
    scenario: str
    objectives: tuple[str, ...]
    failure: str
    setup: str
    experiment: str
    evaluation: str
    production: str


COURSES = [
    Course(
        "curriculum/advanced/14-prompt-evaluation/14_prompt_evaluation.ipynb", 14, "Prompt Evaluation",
        "Northstar must decide whether a new support router is safe to release, including a critical boundary case.",
        ("Retain metric numerators and denominators.", "Compare a baseline and candidate on identical cases.", "Fail a release on any critical regression."),
        "Aggregate accuracy can hide a critical failure in a small slice.",
        """
from lab14 import EvalCase, evaluate, intent_candidate, keyword_baseline, release_allowed

cases = [
    EvalCase("refund", "I want my money back", "refund", "direct"),
    EvalCase("login", "I cannot login", "technical", "direct"),
    EvalCase("boundary", "I read the refund policy; help fix a snapped handle", "technical", "boundary", "critical"),
    EvalCase("hours", "When do you open?", "other", "direct"),
]
""",
        """
baseline = evaluate(keyword_baseline, cases)
candidate = evaluate(intent_candidate, cases)
print("baseline", baseline)
print("candidate", candidate)
print("candidate release allowed:", release_allowed(candidate))
""",
        """
assert baseline.total == candidate.total == 4
assert baseline.critical_failures == ("boundary",)
assert candidate.by_slice["boundary"] == (1, 1)
assert release_allowed(candidate)
""",
        "Keep labelled cases versioned, review slice deltas, and use deterministic checks for schemas and forbidden outcomes. Semantic judges complement—not replace—these gates.",
    ),
    Course(
        "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/15_llm_as_a_judge_and_human_evaluation.ipynb", 15, "LLM-as-a-Judge and Human Evaluation",
        "A support team calibrates a rubric judge against human labels before using it for low-risk triage.",
        ("Write observable rubric criteria.", "Measure judge–human agreement.", "Route ambiguous and high-impact cases to people."),
        "A plausible judge score is not ground truth and may contain position, style, or self-preference bias.",
        """
from lab15 import agreement, pairwise_winner, requires_human_review, rubric_judge

responses = {
    "weak": "We received your message.",
    "strong": "We are sorry. We will replace the mug immediately.",
}
judgements = [rubric_judge(case_id, text) for case_id, text in responses.items()]
human_scores = {"weak": 1, "strong": 5}
""",
        """
print(judgements)
print("exact agreement", agreement(judgements, human_scores))
print("pairwise winner", pairwise_winner(responses["weak"], responses["strong"]))
for judgement in judgements:
    print(judgement.case_id, "human review:", requires_human_review(judgement, high_impact=False))
""",
        """
assert agreement(judgements, human_scores) == (2, 2)
assert pairwise_winner(responses["weak"], responses["strong"]) == "right"
assert requires_human_review(rubric_judge("ambiguous", "Sorry."), high_impact=False)
""",
        "Calibrate on held-out, double-scored examples; log rubric version and reason codes; periodically re-check disagreement and subgroup slices. Never request or store hidden chain-of-thought.",
    ),
    Course(
        "curriculum/advanced/16-evaluation-driven-prompt-optimization/16_evaluation_driven_prompt_optimization.ipynb", 16, "Evaluation-Driven Prompt Optimization",
        "Northstar fixes ticker normalization without tuning on the final test set.",
        ("Separate development and holdout data.", "Score component and joint outcomes.", "Reject a local fix that causes a global regression."),
        "Optimizing on one visible failure leaks evaluation data and can overfit the prompt.",
        """
from lab16 import ExtractionCase, alias_policy, baseline_policy, score, split_cases

cases = [
    ExtractionCase("d1", "$GOOG rallies on AI", "Google", "positive", "development"),
    ExtractionCase("d2", "Northstar posts profit", "Northstar", "positive", "development"),
    ExtractionCase("h1", "$MSFT reports growth", "Microsoft", "positive", "holdout"),
    ExtractionCase("h2", "Acme faces lawsuit", "Acme", "negative", "holdout"),
]
""",
        """
for split in ("development", "holdout"):
    rows = split_cases(cases, split)
    print(split, score("baseline", baseline_policy, rows))
    print(split, score("alias", alias_policy, rows))
""",
        """
development = score("alias", alias_policy, split_cases(cases, "development"))
holdout = score("alias", alias_policy, split_cases(cases, "holdout"))
assert development.joint_accuracy == 1.0
assert holdout.joint_accuracy == 1.0
assert {case.case_id for case in split_cases(cases, "development")}.isdisjoint({case.case_id for case in split_cases(cases, "holdout")})
""",
        "Freeze the contract and holdout before searching. Version the prompt, dataset, model settings, and metric code together; release only after slice and safety gates pass.",
    ),
    Course(
        "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/17_automatic_prompt_optimization_and_dspy.ipynb", 17, "Automatic Prompt Optimization and DSPy",
        "A bounded optimizer selects an extraction strategy on development cases, then receives one chance on the sealed holdout.",
        ("Define a metric before search.", "Constrain the candidate space and budget.", "Evaluate the selected candidate on untouched data."),
        "An optimizer can exploit metric shortcuts or memorize exposed answers.",
        """
from lab17 import PromptCandidate, SearchCase, after_marker, evaluate_holdout, last_token_baseline, select_on_development

cases = [
    SearchCase("city: San Francisco; state: CA", "San Francisco", "development"),
    SearchCase("city: Montréal; country: Canada", "Montréal", "development"),
    SearchCase("city: Vancouver; country: Canada", "Vancouver", "holdout"),
]
candidates = [PromptCandidate("last-token", last_token_baseline), PromptCandidate("marker", after_marker)]
""",
        """
selected = select_on_development(candidates, cases)
print("selected", selected.name)
print("holdout", evaluate_holdout(selected, cases))
""",
        """
assert selected.name == "marker"
assert evaluate_holdout(selected, cases) == (1, 1)
""",
        "Production optimizers need search budgets, traceable trials, protected holdouts, semantic-review samples, rollback, and a human-owned objective. DSPy packages this loop; it does not remove evaluation design work.",
    ),
    Course(
        "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/18_agent_and_multi_agent_prompt_contracts.ipynb", 18, "Agent and Multi-Agent Prompt Contracts",
        "A support router may look up an order or summarize evidence, but only inside the authenticated tenant and a bounded step budget.",
        ("Validate typed tasks at the boundary.", "Authorize before capability exposure.", "Compare a single workflow with a multi-agent design."),
        "A model-generated tenant, approval, or role is untrusted and cannot authorize work.",
        """
from lab18 import AgentTask, architecture_cost, route
from northstar.security import Principal

owner = Principal(user_id="u1", tenant="northstar", roles={"support_agent"})
intruder = Principal(user_id="u2", tenant="other", roles={"support_agent"})
task = AgentTask(task_id="T1", tenant="northstar", kind="lookup", payload={"order_id": "O1"}, max_steps=2)
""",
        """
print("owner", route(task, owner))
print("cross-tenant", route(task, intruder))
print("single workflow cost", architecture_cost(agents=1, model_calls=2, handoffs=0))
print("three-agent cost", architecture_cost(agents=3, model_calls=4, handoffs=2))
""",
        """
assert route(task, owner).status == "completed"
assert route(task, intruder).reason_code == "tenant_mismatch"
assert architecture_cost(agents=1, model_calls=2, handoffs=0) < architecture_cost(agents=3, model_calls=4, handoffs=2)
""",
        "Use narrow tools, explicit terminal states, idempotency keys, bounded retries, durable state only where needed, and approval before consequential side effects. Add agents only when measured decomposition benefits exceed coordination cost.",
    ),
    Course(
        "curriculum/advanced/19-prompting-for-coding-agents/19_prompting_for_coding_agents.ipynb", 19, "Prompting for Coding Agents",
        "A coding agent receives a one-file authentication fix with an exact verification command and no production authority.",
        ("Write a software-change contract.", "Enforce read, write, network, and command scope.", "Require tests and diff evidence before completion."),
        "A prompt saying 'stay in scope' is guidance, not a sandbox or policy boundary.",
        """
from lab19 import ChangeContract, ProposedChange, completion_allowed, validate_plan

contract = ChangeContract(
    problem="Correct the token expiration default from zero to 3600 seconds.",
    allowed_files=("src/auth.py",),
    test_command=("pytest", "tests/test_auth.py"),
    acceptance=("auth tests pass", "only src/auth.py changes"),
)
""",
        """
unsafe = ProposedChange(
    files_to_read=("src/auth.py", "secrets.env"),
    files_to_write=("src/auth.py", "deploy.yml"),
    command=("curl", "production"),
)
safe = ProposedChange(
    files_to_read=("src/auth.py",),
    files_to_write=("src/auth.py",),
    command=("pytest", "tests/test_auth.py"),
)
print("unsafe violations", validate_plan(contract, unsafe))
print("safe violations", validate_plan(contract, safe))
""",
        """
assert set(validate_plan(contract, unsafe)) == {"read_scope", "write_scope", "command_not_approved", "network_not_approved"}
assert validate_plan(contract, safe) == ()
assert completion_allowed(contract, tests_passed=True, diff_files=("src/auth.py",))
""",
        "Run agents in isolated worktrees or sandboxes, grant least privilege, inspect untrusted issues and repository text as data, and verify the actual diff and tests. Production deployment remains a separately authorized action.",
    ),
    Course(
        "curriculum/advanced/20-model-aware-prompt-engineering/20_model_aware_prompt_engineering.ipynb", 20, "Model-Aware Prompt Engineering",
        "Northstar compares model profiles behind one typed contract rather than scattering provider-specific behavior across the application.",
        ("Separate durable contracts from provider adapters.", "Compare quality, schema validity, latency, and cost.", "Choose by measured constraints, not model branding."),
        "A model migration can change output, tool use, latency, safety behavior, and token accounting.",
        """
from lab20 import Entity, ModelProfile, choose_profile, run_trial

text = "Google was founded in 1998 as a search company."
expected = Entity(company="Google", year=1998, industry="search")
profiles = [
    ModelProfile("small", True, 32000, 70, 3),
    ModelProfile("large", True, 1000000, 240, 12),
]
""",
        """
trials = [run_trial(profile, text, expected) for profile in profiles]
for trial in trials:
    print(trial)
print("selected", choose_profile(trials, latency_budget_ms=100, cost_budget=5))
""",
        """
assert all(trial.correct and trial.contract_valid for trial in trials)
assert choose_profile(trials, latency_budget_ms=100, cost_budget=5) == "small"
assert choose_profile(trials, latency_budget_ms=50, cost_budget=5) is None
""",
        "Maintain provider conformance tests, pin known-good configurations, observe model and adapter versions, test migrations on fixed slices, and preserve a rollback path. Capabilities and prices are time-sensitive operational data.",
    ),
    Course(
        "curriculum/advanced/21-cost-latency-and-token-engineering/21_cost_latency_and_token_engineering.ipynb", 21, "Cost, Latency, and Token Engineering",
        "A support answer must retain a termination clause while reducing irrelevant context.",
        ("Trace quality, tokens, latency, and cost together.", "Identify dominated configurations.", "Refuse optimizations that cross a quality gate."),
        "Removing the relevant clause makes a policy cheap and fast but unusable.",
        """
from lab21 import dominates, quality_gate, run_policy

boilerplate = "General terms. " * 80
clause = "The company may terminate with 30 days notice."
full = run_policy("full", boilerplate + clause, "May the company terminate?")
pruned = run_policy("pruned", clause, "May the company terminate?")
lossy = run_policy("lossy", boilerplate, "May the company terminate?")
""",
        """
for result in (full, pruned, lossy):
    print(result, "quality", quality_gate(result, "yes"))
print("pruned dominates full", dominates(pruned, full, expected="yes"))
""",
        """
assert quality_gate(full, "yes") and quality_gate(pruned, "yes")
assert not quality_gate(lossy, "yes")
assert dominates(pruned, full, expected="yes")
assert not dominates(lossy, full, expected="yes")
""",
        "Optimize in this order: remove unnecessary work, route by measured need, bound outputs and retries, cache only within authorization scope, then consider model changes. Report percentiles and quality-adjusted cost by slice.",
    ),
    Course(
        "curriculum/enterprise/22-promptops/22_promptops.ipynb", 22, "PromptOps",
        "Northstar promotes a complete behavior artifact only when reproducible quality and safety gates pass.",
        ("Version the full behavior artifact.", "Make release policy deterministic.", "Compare artifacts and preserve rollback evidence."),
        "Versioning only prompt text omits schema, model settings, evaluation data, and ownership.",
        """
from lab22 import BehaviorArtifact, GateInput, compare_artifacts, release_gate

baseline = BehaviorArtifact("1.0", "classify", "1", "model-a@0", "eval@1", "support-ai")
candidate = BehaviorArtifact("1.1", "classify by user intent", "1", "model-a@0", "eval@2", "support-ai")
passing = GateInput(99, 100, 0, 0)
critical = GateInput(100, 100, 1, 0)
""",
        """
print("baseline digest", baseline.digest)
print("candidate digest", candidate.digest)
print("changed fields", compare_artifacts(baseline, candidate))
print("passing gate", release_gate(passing))
print("critical gate", release_gate(critical))
""",
        """
assert baseline.digest != candidate.digest
assert release_gate(passing)[0]
assert not release_gate(critical)[0]
""",
        "Store immutable artifacts and evaluation reports, require accountable review for risk changes, deploy progressively, correlate production traces to an artifact digest, and rehearse rollback.",
    ),
    Course(
        "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/23_prompt_observability_and_failure_diagnosis.ipynb", 23, "Prompt Observability and Failure Diagnosis",
        "A wrong price answer must be traced to stale evidence without logging customer email addresses or hidden reasoning.",
        ("Capture correlated structured spans.", "Redact sensitive attributes.", "Diagnose the first observable failing layer."),
        "A complete transcript can leak data while still omitting the version and freshness fields needed for diagnosis.",
        """
from lab23 import diagnose, safe_span

healthy = [
    safe_span("trace-1", "retrieve", "ok", 18, {"query": "user@example.com", "evidence_fresh": True, "source_version": "v2"}),
    safe_span("trace-1", "generate", "ok", 70, {"schema_valid": True, "model": "fixture"}),
]
stale = [
    safe_span("trace-2", "retrieve", "ok", 17, {"query": "user@example.com", "evidence_fresh": False, "source_version": "v1"}),
    safe_span("trace-2", "generate", "ok", 68, {"schema_valid": True, "model": "fixture"}),
]
""",
        """
print("healthy diagnosis", diagnose(healthy))
print("stale diagnosis", diagnose(stale))
print("redacted query", stale[0].attributes["query"])
""",
        """
assert diagnose(healthy) == "no_observed_failure"
assert diagnose(stale) == "stale_evidence"
assert stale[0].attributes["query"] == "[REDACTED_EMAIL]"
""",
        "Emit trace IDs, artifact/model/tool versions, policy results, evidence IDs, latency, usage, errors, and terminal state. Minimize content capture, set retention controls, and align names with OpenTelemetry conventions where stable.",
    ),
    Course(
        "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/24_prompt_versioning_experimentation_and_release_engineering.ipynb", 24, "Prompt Versioning, Experimentation, and Release Engineering",
        "A candidate is routed by a stable request key and rolled back only with enough evidence—or immediately after a critical failure.",
        ("Use deterministic, sticky assignment.", "Separate insufficient samples from success.", "Make critical rollback conditions explicit."),
        "Random per-request assignment breaks user consistency and makes incident reconstruction difficult.",
        """
from lab24 import CanaryEvidence, route_version, should_rollback

assignments = {request_id: route_version(request_id, canary_percent=20) for request_id in [f"R-{i}" for i in range(30)]}
print(assignments)
""",
        """
early = CanaryEvidence(requests=3, failures=1, critical_failures=0)
mature = CanaryEvidence(requests=100, failures=8, critical_failures=0)
critical = CanaryEvidence(requests=1, failures=1, critical_failures=1)
for evidence in (early, mature, critical):
    print(evidence, should_rollback(evidence))
""",
        """
assert route_version("R-1", canary_percent=20) == route_version("R-1", canary_percent=20)
assert should_rollback(early)[1] == "insufficient_samples"
assert should_rollback(mature) == (True, "failure_rate")
assert should_rollback(critical) == (True, "critical_failure")
""",
        "Pre-register metrics and guardrails, preserve cohort assignment, compare the same slices, define minimum samples and stop rules, and keep a tested stable artifact ready for rollback.",
    ),
    Course(
        "curriculum/enterprise/25-prompt-governance-and-responsible-ai/25_prompt_governance_and_responsible_ai.ipynb", 25, "Prompt Governance and Responsible AI",
        "A high-risk support artifact may ship only with an active, policy-versioned approval from the trusted governance registry.",
        ("Connect policy to executable controls.", "Keep ownership and prohibited uses explicit.", "Use trusted approval records rather than model claims."),
        "A mutable boolean inside a manifest or model output is not auditable approval.",
        """
from lab25 import Approval, GovernanceManifest, governance_gate

manifest = GovernanceManifest(
    artifact_id="support-finance-v2", artifact_digest="aaaaaaaaaaaaaaaa", owner="support-ai", risk_tier="high",
    handles_personal_data=True, intended_use="explain billing records", prohibited_uses=("credit decision",),
)
NOW = 2_000
valid = Approval("APR-1", "support-finance-v2", manifest.artifact_digest, "reviewer-7", "risk_board", "policy-2026-2", 3_000, "active")
wrong_version = Approval("APR-2", "support-finance-v2", manifest.artifact_digest, "reviewer-7", "risk_board", "policy-2025-4", 3_000, "active")
""",
        """
print("no approval", governance_gate(manifest, [], policy_version="policy-2026-2", now=NOW))
print("stale approval", governance_gate(manifest, [wrong_version], policy_version="policy-2026-2", now=NOW))
print("valid approval", governance_gate(manifest, [valid], policy_version="policy-2026-2", now=NOW))
""",
        """
assert not governance_gate(manifest, [], policy_version="policy-2026-2", now=NOW).allowed
assert not governance_gate(manifest, [wrong_version], policy_version="policy-2026-2", now=NOW).allowed
assert governance_gate(manifest, [valid], policy_version="policy-2026-2", now=NOW).allowed
""",
        "Maintain policy/control/evidence traceability, named owners, exception expiry, audit retention, incident escalation, and jurisdiction-specific review. Reassess when use, data, model, or policy changes.",
    ),
    Course(
        "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/26_human_centred_ai_and_trust_calibration.ipynb", 26, "Human-Centred AI and Trust Calibration",
        "An industrial-support answer with high claimed confidence still requires human review when it proposes bypassing a safety control.",
        ("Calibrate confidence against outcomes.", "Tie escalation to impact and evidence.", "Expose user-facing uncertainty without hidden reasoning."),
        "Self-reported confidence is not permission and can be badly calibrated.",
        """
from lab26 import ProposedAnswer, calibration_error, decide_delivery

known = {"manual-X900-v4"}
safe = ProposedAnswer("Use the documented reset procedure.", 0.9, ("manual-X900-v4",), "low")
dangerous = ProposedAnswer("Bypass the regulator.", 0.99, ("manual-X900-v4",), "high")
unsupported = ProposedAnswer("Change internal wiring.", 0.95, ("invented",), "medium")
""",
        """
for answer in (safe, dangerous, unsupported):
    print(answer.response, "=>", decide_delivery(answer, known))
print("calibration error", calibration_error([(0.9, True), (0.8, False), (0.6, True)]))
""",
        """
assert decide_delivery(safe, known).state == "answer"
assert decide_delivery(dangerous, known).state == "human_review"
assert decide_delivery(unsupported, known).state == "blocked"
assert 0 <= calibration_error([(0.9, True), (0.8, False)]) <= 1
""",
        "Design review queues with ownership and service levels, show sources and limitations to users, measure override and harm outcomes, prevent automation bias, and never log private chain-of-thought as an explanation.",
    ),
    Course(
        "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/27_prompt_portability_and_multi_model_systems.ipynb", 27, "Prompt Portability and Multi-Model Systems",
        "Two provider adapters must satisfy one output contract; failover is permitted for a read-only summary but not an unconfirmed side effect.",
        ("Normalize provider responses at adapters.", "Run the same conformance fixtures across providers.", "Constrain fallback by operation semantics."),
        "Blind failover can duplicate writes, change policy behavior, or silently return incompatible output.",
        """
from lab27 import FixtureAdapter, Summary, conformance, route

text = "Acme Corp reports a revenue drop due to supply chain issues."
expected = Summary(company="Acme Corp", revenue_trend="DOWN", risks=("supply chain",))
primary = FixtureAdapter("primary")
fallback = FixtureAdapter("fallback")
outage = FixtureAdapter("primary", available=False)
""",
        """
print("primary conformance", conformance(primary, [(text, expected)]))
print("fallback conformance", conformance(fallback, [(text, expected)]))
print("normal route", route(primary, fallback, text, operation_is_read_only=True))
print("outage route", route(outage, fallback, text, operation_is_read_only=True))
""",
        """
assert conformance(primary, [(text, expected)]) == (1, 1)
assert route(outage, fallback, text, operation_is_read_only=True).fallback_used
try:
    route(outage, fallback, text, operation_is_read_only=False)
except RuntimeError as error:
    assert "unsafe_fallback" in str(error)
else:
    raise AssertionError("side-effecting failover was allowed")
""",
        "Pin adapter and provider versions, normalize errors and usage, test schemas and safety policy per provider, enforce idempotency for retries, and decide whether degraded mode should abstain rather than silently switch.",
    ),
    Course(
        "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/28_prompt_architecture_patterns_and_system_selection.ipynb", 28, "Prompt Architecture Patterns and System Selection",
        "Northstar selects the least complex architecture that meets auditability, adaptability, latency, and operating-cost needs.",
        ("Turn requirements into explicit criteria.", "Expose the score behind a recommendation.", "Test whether the winner changes under plausible weights."),
        "A single weighted score can disguise fragile assumptions and false precision.",
        """
from lab28 import Architecture, select_architecture, sensitivity

options = [
    Architecture("single-call", 4, 1, 5, 3, 5),
    Architecture("workflow", 5, 3, 4, 5, 3),
    Architecture("agent", 2, 5, 2, 2, 1),
]
weights = {"determinism": 3, "adaptability": 1, "latency": 2, "auditability": 3, "operational_cost": 1}
""",
        """
winner, scores = select_architecture(options, weights)
print("winner", winner)
print("scores", scores)
weight_sets = [weights, {**weights, "adaptability": 6}, {**weights, "operational_cost": 5}]
print("sensitivity", sensitivity(options, weight_sets))
""",
        """
assert winner == "workflow"
assert sum(sensitivity(options, weight_sets).values()) == len(weight_sets)
assert set(scores) == {item.name for item in options}
""",
        "Prototype the top two options on representative cases. Include failure recovery, authorization, observability, skill availability, team capacity, and total operating cost—not only model quality.",
    ),
    Course(
        "curriculum/enterprise/29-ai-system-engineering-capstone/29_ai_system_engineering_capstone.ipynb", 29, "AI System Engineering Capstone",
        "A release board reviews a portfolio of executable evidence rather than accepting a polished demo or checklist claim.",
        ("Assemble contract, evaluation, threat, trace, ownership, and rollback evidence.", "Run a fail-closed readiness gate.", "Distinguish missing evidence from failed evidence."),
        "A green average score cannot override critical failures, missing ownership, or an untested rollback.",
        """
from lab29 import CapstoneSubmission, REQUIRED_EVIDENCE, evaluate_readiness, evidence_artifact

incomplete = CapstoneSubmission("northstar-capstone", {"owner": "support-ai"}, critical_failures=0, tests_passed=True)
artifact_store = {
    f"artifacts/{name}.md": f"verified {name}"
    for name in REQUIRED_EVIDENCE
}
complete = CapstoneSubmission(
    "northstar-capstone",
    {
        name: evidence_artifact(f"artifacts/{name}.md", artifact_store[f"artifacts/{name}.md"])
        for name in REQUIRED_EVIDENCE
    },
    critical_failures=0,
    tests_passed=True,
)
""",
        """
print("incomplete", evaluate_readiness(incomplete, artifact_store))
print("complete", evaluate_readiness(complete, artifact_store))
""",
        """
assert not evaluate_readiness(incomplete, artifact_store).ready
assert set(evaluate_readiness(incomplete, artifact_store).missing) == REQUIRED_EVIDENCE - {"owner"}
assert evaluate_readiness(incomplete, artifact_store).invalid == ("owner",)
assert evaluate_readiness(complete, artifact_store).ready
""",
        "The final review must reproduce the offline path, examine critical and slice failures, inspect least-privilege controls, verify trace privacy, name owners and SLOs, and rehearse rollback before production authority is granted.",
    ),
]


# Chapter metadata is deliberately separate from executable notebook cells.
GUIDES = {
    14: "../../../docs/07-evaluation.md", 15: "../../../docs/07-evaluation.md",
    16: "../../../docs/21-evaluation-driven-prompt-optimization.md", 17: "../../../docs/21-evaluation-driven-prompt-optimization.md",
    18: "../../../docs/08-agentic-prompts.md", 19: "../../../docs/12-coding-agent-prompting.md",
    20: "../../../docs/16-model-aware-guidance.md", 21: "../../../docs/13-cost-latency-engineering.md",
    22: "../../../docs/09-promptops.md", 23: "../../../docs/09-promptops.md", 24: "../../../docs/09-promptops.md",
    25: "../../../docs/19-reliability-and-human-centred-ai.md", 26: "../../../docs/19-reliability-and-human-centred-ai.md",
    27: "../../../docs/10-technology-review.md", 28: "../../../docs/10-technology-review.md", 29: "../../../docs/10-technology-review.md",
}

LANDSCAPES = {
    14: "Use exact validators for typed outcomes, rubric review for semantic outcomes, and trajectory checks for tools. Frameworks can schedule evals; they cannot define the product's correct metric.",
    15: "Absolute scoring supports rubric dimensions; pairwise comparison needs order swaps and ties; human review establishes labels and adjudicates ambiguity. Judges remain probabilistic components.",
    16: "Manual hypothesis testing is easiest to audit. Search tools become valuable only after the contract, development split, protected holdout, safety constraints, and budget are explicit.",
    17: "DSPy and related optimizers compile prompt programs against a metric. Bounded search must still be checked for leakage and metric gaming.",
    18: "Prefer deterministic code, then a single call, then a fixed workflow. Use agents only when measured dynamic-work benefits exceed coordination cost.",
    19: "Coding-agent interfaces differ, but the portable controls are scoped instructions, untrusted-input handling, least privilege, tests, diff inspection, and separate deployment authority.",
    20: "Managed APIs, cloud endpoints, and self-hosted models trade operational control, data boundaries, latency, and cost. Adapters improve testability but do not erase capability differences. Native schema support is a provider capability, while `contract_valid` records whether the normalized application output actually passed validation; a tested adapter can provide the latter without claiming the former.",
    21: "Caching, routing, pruning, batching, parallel reads, and model allocation solve different bottlenecks. Use real tokenizers and measured latency in production.",
    22: "Git and CI may be sufficient at first. Add registries, evaluation platforms, tracing, and flags when team, artifact, or audit scale justifies them.",
    23: "Standard traces improve portability. OpenTelemetry's generative-AI conventions are evolving, so pin a version and avoid sensitive content capture by default.",
    24: "Shadow evaluation, canaries, and A/B tests answer different questions. All need stable assignment, declared metrics, guardrails, enough samples, and rollback policy.",
    25: "Governance combines policy, controls, evidence, approval, and accountability. The lab's trusted approval record is bound to an artifact digest, approver identity and role, policy version, state, and expiry; changing any binding invalidates approval. Provider filters are layers, not substitutes for legal analysis or application authorization.",
    26: "Citation interfaces, editable drafts, review queues, and uncertainty signals can help. Token probabilities and self-reported confidence are not generally calibrated factuality measures.",
    27: "Direct adapters maximize provider features; gateways centralize routing; self-hosting increases operational control. Measure contract conformance, quality, safety, latency, and cost.",
    28: "Single calls, retrieval, tools, workflows, and agents form a complexity ladder. Selection is a requirements and evidence exercise, not a popularity contest.",
    29: "The capstone is framework-neutral. Its readiness gate recomputes each submitted SHA-256 digest against content from a separately supplied artifact store; a filename, checklist string, or self-attested flag is not proof. Add orchestration only after contracts, identity, evidence, evaluation, tracing, and release policy are proven.",
}

OFFICIAL_REFERENCES = {
    14: [("OpenAI evaluation guide", "https://developers.openai.com/api/docs/guides/evals"), ("G-Eval paper", "https://arxiv.org/abs/2303.16634")],
    15: [("G-Eval paper", "https://arxiv.org/abs/2303.16634"), ("Judging LLM-as-a-Judge", "https://arxiv.org/abs/2306.05685")],
    16: [("OpenAI evaluation guide", "https://developers.openai.com/api/docs/guides/evals")],
    17: [("DSPy optimizers", "https://dspy.ai/learn/optimization/optimizers/"), ("DSPy repository", "https://github.com/stanfordnlp/dspy")],
    18: [("Google function calling", "https://ai.google.dev/gemini-api/docs/function-calling"), ("Anthropic: building effective agents", "https://www.anthropic.com/engineering/building-effective-agents")],
    19: [("OWASP secure coding with AI", "https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html")],
    20: [("Google models", "https://ai.google.dev/gemini-api/docs/models"), ("Google structured output", "https://ai.google.dev/gemini-api/docs/structured-output")],
    21: [("Google token counting", "https://ai.google.dev/gemini-api/docs/tokens"), ("OpenAI latency optimization", "https://developers.openai.com/api/docs/guides/latency-optimization")],
    22: [("OpenTelemetry semantic conventions", "https://opentelemetry.io/docs/specs/semconv/")],
    23: [("OpenTelemetry GenAI conventions", "https://github.com/open-telemetry/semantic-conventions-genai")],
    24: [("OpenFeature specification", "https://openfeature.dev/specification/")],
    25: [("NIST Generative AI Profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence"), ("OWASP prompt-injection prevention", "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html")],
    26: [("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework")],
    27: [("Google structured output", "https://ai.google.dev/gemini-api/docs/structured-output"), ("OpenTelemetry GenAI conventions", "https://github.com/open-telemetry/semantic-conventions-genai")],
    28: [("Berkeley: Compound AI Systems", "https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/")],
    29: [("NIST Generative AI Profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence"), ("OWASP AI Agent Security", "https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html")],
}


def markdown(course: Course, heading: str, body: str) -> str:
    return dedent(f"""
    ## {heading}

    {body}
    """).strip()


def build(course: Course) -> nbformat.NotebookNode:
    objectives = "\n".join(f"- {item}" for item in course.objectives)
    introduction = dedent(f"""
    # {course.number:02d} — {course.title}

    ## Scenario and success criteria

    {course.scenario}

    This guided lab succeeds when its assertions pass and the learner can explain why the baseline fails, what the mitigation changes, and which production controls remain outside the simulation.

    ## Learning objectives

    {objectives}

    **Prerequisites:** Courses 01–13 and the preceding advanced/enterprise lesson.
    **Safety boundary:** all behavior is deterministic and synthetic; there are no credentials, external calls, or side effects. Printed results are simulation evidence, not a live-model benchmark.
    """).strip()
    architecture = dedent(f"""
    ## Mental model and architecture

    ![Course {course.number:02d} architecture](diagram-1.svg)

    Treat the model as one uncertain component inside a deterministic control plane. Inputs, schemas, identity, authorization, metrics, release gates, and state transitions remain application responsibilities.

    ## Baseline and failure injection

    {course.failure}

    The next cell defines the synthetic fixture and the smallest reusable primitive needed to make that failure observable.
    """).strip()
    evaluation = dedent(f"""
    ## Evaluation

    The assertions below are the executable contract. They validate both a positive path and a boundary or failure path; a printed claim alone is not proof.
    """).strip()
    production = dedent(f"""
    ## Production upgrade

    {course.production}

    | Teaching lab | Production system |
    | --- | --- |
    | Synthetic fixtures | Versioned, reviewed, privacy-safe datasets |
    | Deterministic simulation | Provider adapter plus optional recorded replay |
    | In-process state | Durable state with tenant and retention boundaries |
    | Assertions | CI gates, staged rollout, monitoring, and rollback |

    ## Exercises

    1. Add one normal, one boundary, and one adversarial case without weakening an invariant.
    2. Change one design variable and report the metric numerator, denominator, unit, and direction.
    3. Write a production decision memo that identifies owner, failure policy, monitoring signal, and rollback trigger.

    ## Takeaway

    Use probabilistic components for bounded interpretation; use trusted deterministic code for permissions, validation, metrics, and consequential state changes.
    """).strip()
    cells = [
        nbformat.v4.new_markdown_cell(introduction),
        nbformat.v4.new_markdown_cell(architecture),
        nbformat.v4.new_code_cell(dedent(course.setup).strip()),
        nbformat.v4.new_markdown_cell(markdown(course, "Experiment", "Run the baseline and candidate on the same fixture so the comparison is attributable.")),
        nbformat.v4.new_code_cell(dedent(course.experiment).strip()),
        nbformat.v4.new_markdown_cell(evaluation),
        nbformat.v4.new_code_cell(dedent(course.evaluation).strip()),
        nbformat.v4.new_markdown_cell(production),
    ]
    for index, cell in enumerate(cells, start=1):
        cell.id = f"course-{course.number:02d}-cell-{index:02d}"
    notebook = nbformat.v4.new_notebook(cells=cells)
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata.language_info = {"name": "python", "version": "3.12"}
    return notebook


def build_readme(course: Course) -> str:
    notebook = Path(course.path).name
    lab = f"lab{course.number}.py"
    objectives = "\n".join(f"- {item}" for item in course.objectives).replace("\n", "\n    ")
    references = "\n".join(
        f"- [{label}]({url})" for label, url in OFFICIAL_REFERENCES[course.number]
    ).replace("\n", "\n    ")
    capstone = ""
    if course.number == 29:
        capstone = dedent("""
        ## Milestone notebooks

        1. [Foundation](milestones/01_milestone_foundation.ipynb)
        2. [RAG and tools](milestones/02_milestone_rag_and_tools.ipynb)
        3. [Routing and security](milestones/03_milestone_routing_and_security.ipynb)
        4. [Portability](milestones/04_milestone_portability.ipynb)
        5. [Production release](milestones/05_milestone_production_release.ipynb)
        """).strip().replace("\n", "\n    ")
    return dedent(f"""
    # {course.number:02d} — {course.title}

    ## Learning outcomes

    {objectives}

    ## Why this matters

    {course.scenario} A persuasive demonstration is not sufficient evidence: the system must expose its inputs, decisions, failures, metrics, and release policy.

    ## Prerequisites, success criteria, and boundaries

    **Prerequisites:** Courses 01–13 plus the preceding lesson in this track. Learners should be comfortable with Python, typed data, fixtures, exact assertions, and basic evaluation terminology.

    **Success criteria:** the [notebook]({notebook}) runs without credentials, its positive and failure assertions pass, and the learner can explain which controls are deterministic and which production behaviors would remain probabilistic.

    **Non-goals:** this course does not claim that a small deterministic fixture predicts live-model quality, and it does not grant production access or make provider benchmarks.

    **Risk boundary:** identity, authorization, schemas, arithmetic, release gates, and consequential state changes belong to trusted application code. Model output may propose or interpret; it may not authorize itself.

    ## Mental model

    ![{course.title} architecture](diagram-1.svg)

    Treat the AI feature as a versioned behavior system:

    ```text
    contract + context + model/adapter + deterministic controls
        -> observable result + evidence + metrics + terminal state
        -> release, abstain, review, block, or rollback
    ```

    This split matters because a schema or prompt can constrain a proposal, while the application still owns validation and policy enforcement.

    ## Foundations and internal mechanics

    1. **Define the decision.** State the input, expected outcome, risk, and terminal states before choosing a model or framework.
    2. **Make evidence executable.** Use labelled fixtures, exact invariants, and named failure cases. Printed expected values and comments are not tests.
    3. **Retain measurement semantics.** Record numerator, denominator, slice, unit, and direction. Separate blocked attempts from completed violations and estimates from provider-reported usage.
    4. **Keep a reproducible path.** The default lab is synthetic and credential-free. A live provider is an optional experiment that needs its own versioned results.

    ## Architecture and technology choices

    {LANDSCAPES[course.number]}

    Choose the smallest architecture that can satisfy the behavior contract. Framework adoption is a downstream decision; it does not replace the contract, fixtures, controls, or release evidence.

    ## Worked Northstar scenario

    The [reusable lab]({lab}) implements the deterministic primitive. The notebook introduces the scenario, runs the baseline and candidate on the same fixture, injects this failure—**{course.failure}**—and finishes with assertions plus a production-upgrade exercise.

    Run it from the repository root:

    ```bash
    PYTHONPATH=. .venv/bin/python scripts/run_notebooks.py {course.path}
    .venv/bin/python -m pytest -q tests/test_advanced_enterprise_labs.py
    ```

    ## Evaluation design

    | Case family | What it proves | Release treatment |
    | --- | --- | --- |
    | Normal | Main behavior works on representative input | Count in the named quality metric |
    | Boundary | Ambiguity and limits are explicit | Review by slice; do not average away |
    | Failure | Recovery or terminal state is correct | Must produce the expected reason code |
    | Critical/adversarial | Forbidden disclosure or action is prevented | Hard blocker, independent of mean score |

    Evaluation should compare a baseline and candidate on identical cases. Development data may guide changes; a protected holdout supports the final claim. Re-run evaluation when the prompt, context policy, schema, tools, model, adapter, or metric implementation changes.

    ## Failure modes and mitigations

    - **Metric gaming:** test whether a candidate exploits formatting or label leakage; use review samples and protected data.
    - **False authority:** derive identity, tenant, roles, and approval from trusted state before retrieval or tool exposure.
    - **Silent degradation:** make abstention, blocked, retryable, approval-required, and rollback states explicit.
    - **Misleading observability:** log versions, reason codes, evidence IDs, and terminal state without secrets or hidden reasoning.
    - **Framework overreach:** retain a deterministic baseline and add orchestration only when measured value justifies complexity.

    ## Production upgrade

    {course.production}

    Production systems additionally need concurrency handling, bounded retries, idempotency for side effects, tenant-scoped caches and memory, secret management, data-retention policy, service objectives, incident ownership, staged rollout, and a rehearsed rollback path. The exact set depends on risk; it should be recorded in an architecture decision rather than hidden in prompt text.

    ## State of the art

    - **Established:** typed contracts, representative evaluation sets, deterministic validation, least privilege, versioned artifacts, and observable release gates.
    - **Emerging:** standardized generative-AI telemetry, automated evaluation pipelines, learned routing, and optimization frameworks tied to explicit metrics.
    - **Research frontier:** robust semantic judging, prompt-injection resistance, cross-model behavioral equivalence, calibrated uncertainty, and evaluation under distribution shift.

    The frontier is not a default architecture. Adopt an emerging technique only after it beats the simpler baseline on the course's stated quality, safety, latency, and cost criteria.

    ## Checkpoint

    1. Which part of this course's decision must remain in deterministic application code, and why?
    2. Why does the failure case—{course.failure}—invalidate a happy-path-only evaluation?
    3. What evidence would you require before replacing the lab's simulation with a live provider result?

    ## Exercises and review questions

    1. Add one normal, one boundary, and one adversarial fixture. Which metric or hard gate changes?
    2. Replace one deterministic simulation with a recorded provider response and label the provenance. What new variance appears?
    3. Identify one prompt instruction that currently sounds like policy. Move enforcement into code and add a negative test.
    4. Write a short architecture decision covering owner, alternatives, failure policy, monitoring, and rollback.

    {capstone}

    ## References

    - [Deep course guide]({GUIDES[course.number]})
    {references}
    """).strip() + "\n"


def build_milestone(number: int, title: str, evidence_key: str) -> nbformat.NotebookNode:
    cells = [
        nbformat.v4.new_markdown_cell(dedent(f"""
        # Capstone milestone {number}: {title}

        This credential-free milestone creates one auditable evidence record for the Course 29 release portfolio. Replace the synthetic path with your project artifact, then keep the assertion as the completion gate.
        """).strip()),
        nbformat.v4.new_code_cell(dedent(f"""
        from pathlib import PurePosixPath

        evidence_key = {evidence_key!r}
        evidence_path = PurePosixPath("artifacts") / f"{{evidence_key}}.md"
        record = {{"type": evidence_key, "path": str(evidence_path), "reviewed": True}}
        print(record)
        """).strip()),
        nbformat.v4.new_markdown_cell("## Completion gate\n\nThe record must be named, reviewable, and relative to the project root. A notebook output is not a substitute for the actual artifact."),
        nbformat.v4.new_code_cell("assert record[\"reviewed\"]\nassert not evidence_path.is_absolute()\nassert evidence_path.suffix == \".md\""),
        nbformat.v4.new_markdown_cell("## Production handoff\n\nAdd the artifact digest, owner, review date, policy/version scope, and links to the tests or traces that support it."),
    ]
    for index, cell in enumerate(cells, start=1):
        cell.id = f"milestone-{number:02d}-cell-{index:02d}"
    notebook = nbformat.v4.new_notebook(cells=cells)
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata.language_info = {"name": "python", "version": "3.12"}
    return notebook


def main() -> None:
    for course in COURSES:
        path = ROOT / course.path
        nbformat.write(build(course), path)
        print(path.relative_to(ROOT))
        readme_path = path.parent / "README.md"
        readme_path.write_text(build_readme(course), encoding="utf-8")
        print(readme_path.relative_to(ROOT))
    milestones = [
        (1, "foundation", "behavior_contract"),
        (2, "RAG and tools", "evaluation_report"),
        (3, "routing and security", "threat_model"),
        (4, "portability", "trace_sample"),
        (5, "production release", "rollback_plan"),
    ]
    directory = ROOT / "curriculum/enterprise/29-ai-system-engineering-capstone/milestones"
    for number, title, key in milestones:
        path = directory / f"{number:02d}_milestone_{title.replace(' ', '_')}.ipynb"
        existing = sorted(directory.glob(f"{number:02d}_milestone_*.ipynb"))
        if existing:
            path = existing[0]
        nbformat.write(build_milestone(number, title, key), path)
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
