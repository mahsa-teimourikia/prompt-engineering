# 21 — Cost, Latency, and Token Engineering

## Learning outcomes

- Trace quality, tokens, latency, and cost together.
- Identify dominated configurations.
- Refuse optimizations that cross a quality gate.

## Why this matters

A support answer must retain a termination clause while reducing irrelevant context. A persuasive demonstration is not sufficient evidence: the system must expose its inputs, decisions, failures, metrics, and release policy.

## Prerequisites, success criteria, and boundaries

**Prerequisites:** Courses 01–13 plus the preceding lesson in this track. Learners should be comfortable with Python, typed data, fixtures, exact assertions, and basic evaluation terminology.

**Success criteria:** the [notebook](21_cost_latency_and_token_engineering.ipynb) runs without credentials, its positive and failure assertions pass, and the learner can explain which controls are deterministic and which production behaviors would remain probabilistic.

**Non-goals:** this course does not claim that a small deterministic fixture predicts live-model quality, and it does not grant production access or make provider benchmarks.

**Risk boundary:** identity, authorization, schemas, arithmetic, release gates, and consequential state changes belong to trusted application code. Model output may propose or interpret; it may not authorize itself.

## Mental model

![Cost, Latency, and Token Engineering architecture](diagram-1.svg)

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

Caching, routing, pruning, batching, parallel reads, and model allocation solve different bottlenecks. Use real tokenizers and measured latency in production.

Choose the smallest architecture that can satisfy the behavior contract. Framework adoption is a downstream decision; it does not replace the contract, fixtures, controls, or release evidence.

## Worked Northstar scenario

The [reusable lab](lab21.py) implements the deterministic primitive. The notebook introduces the scenario, runs the baseline and candidate on the same fixture, injects this failure—**Removing the relevant clause makes a policy cheap and fast but unusable.**—and finishes with assertions plus a production-upgrade exercise.

Run it from the repository root:

```bash
PYTHONPATH=. .venv/bin/python scripts/run_notebooks.py curriculum/advanced/21-cost-latency-and-token-engineering/21_cost_latency_and_token_engineering.ipynb
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

Optimize in this order: remove unnecessary work, route by measured need, bound outputs and retries, cache only within authorization scope, then consider model changes. Report percentiles and quality-adjusted cost by slice.

Production systems additionally need concurrency handling, bounded retries, idempotency for side effects, tenant-scoped caches and memory, secret management, data-retention policy, service objectives, incident ownership, staged rollout, and a rehearsed rollback path. The exact set depends on risk; it should be recorded in an architecture decision rather than hidden in prompt text.

## State of the art

- **Established:** typed contracts, representative evaluation sets, deterministic validation, least privilege, versioned artifacts, and observable release gates.
- **Emerging:** standardized generative-AI telemetry, automated evaluation pipelines, learned routing, and optimization frameworks tied to explicit metrics.
- **Research frontier:** robust semantic judging, prompt-injection resistance, cross-model behavioral equivalence, calibrated uncertainty, and evaluation under distribution shift.

The frontier is not a default architecture. Adopt an emerging technique only after it beats the simpler baseline on the course's stated quality, safety, latency, and cost criteria.

## Checkpoint

1. Which part of this course's decision must remain in deterministic application code, and why?
2. Why does the failure case—Removing the relevant clause makes a policy cheap and fast but unusable.—invalidate a happy-path-only evaluation?
3. What evidence would you require before replacing the lab's simulation with a live provider result?

## Exercises and review questions

1. Add one normal, one boundary, and one adversarial fixture. Which metric or hard gate changes?
2. Replace one deterministic simulation with a recorded provider response and label the provenance. What new variance appears?
3. Identify one prompt instruction that currently sounds like policy. Move enforcement into code and add a negative test.
4. Write a short architecture decision covering owner, alternatives, failure policy, monitoring, and rollback.



## References

- [Deep course guide](../../../docs/13-cost-latency-engineering.md)
- [Google token counting](https://ai.google.dev/gemini-api/docs/tokens)
- [OpenAI latency optimization](https://developers.openai.com/api/docs/guides/latency-optimization)
