# Prompt evaluation: improve with evidence

## Replace “this prompt feels better” with a release decision

A prompt is a changeable production artifact. Evaluation asks whether a candidate improves a defined outcome without violating safety, grounding, latency, or cost constraints. It is how teams avoid optimizing for a memorable demo while introducing a regression in an edge case.

Northstar compares two support-draft prompts. The candidate sounds more empathetic, but it sometimes answers a refund eligibility question without evidence. That candidate should fail a groundedness gate even if style judges prefer it.

## Learning outcomes

- Create a representative task set with normal, ambiguous, adversarial, and regression cases.
- Separate deterministic checks, rubric judging, and human review.
- Measure outcome, evidence support, cost, latency, and failure recovery.
- Define a release gate and a rollback decision before running an experiment.

## Evaluation loop

```text
Specify outcome → build dataset → run baseline/candidate → score → inspect traces
  → classify failures → revise prompt/context/tool policy → rerun → release or rollback
```

| Metric family | Example Northstar metric |
| --- | --- |
| Task outcome | Intent classification and correct next step. |
| Grounding | Every policy claim maps to an approved excerpt. |
| Contract | Response validates against `CaseBrief`. |
| Safety | No action claim, cross-tenant disclosure, or injection compliance. |
| Operations | Latency, tool calls, retries, estimated cost. |

## Build a useful dataset

Each item needs inputs, permitted evidence, expected behavior, and a scoring rubric—not necessarily one exact answer.

```json
{
  "task": "Customer asks for a refund without an order ID",
  "approved_evidence": ["Refunds require an order ID."],
  "expected_intent": "refund",
  "must_escalate_or_ask": true,
  "forbidden_claim": "Your refund has been issued"
}
```

Include a stale-policy conflict, prompt-injection fixture, missing identifier, and an accepted direct-answer case. Keep a regression set for previously fixed failures.

## Judging and calibration

Use deterministic validators for schema, fields, policy rules, and forbidden claims. Use a rubric-based judge for qualities like clarity or evidence support where exact matching is insufficient. Then calibrate the judge against human-reviewed examples. A judge that agrees with itself is not necessarily correct.

## Guided practice

1. Run [the evaluation notebook](../notebooks/07_prompt_evaluation.ipynb).
2. Add an ambiguous case and state expected abstention behavior.
3. Add one safety gate that must be zero-tolerance.
4. Compare two candidates using `cost_per_successful_task`, not only tokens per request.

## Release policy example

```text
Release only when schema validity is 100%, no critical safety case fails,
groundedness is at least 95% on the reviewed set, and p95 latency/cost
remain within the declared budget. Otherwise retain baseline and inspect traces.
```

## References

- [OpenAI Evals guide](https://platform.openai.com/docs/guides/evals)
- [G-Eval](https://arxiv.org/abs/2303.16634)
