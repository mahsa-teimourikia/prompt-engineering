# PromptOps: model-aware, tested, observable changes

## Treat prompts and context policies as deployable artifacts

PromptOps applies sound delivery practice to prompt, context, examples, schema, tool descriptions, and evaluation data. A production prompt change can alter safety, cost, latency, tool selection, and groundedness. Version it, test it, observe it, and retain a rollback path.

Northstar's candidate prompt may improve customer tone but increase unsupported policy claims. The deployment decision belongs to a release gate with evaluated evidence—not the last person who read an impressive response.

## Learning outcomes

- Version all behavior-shaping artifacts, not only prompt text.
- Compare model/prompt variants against a shared behavioral contract.
- Define release gates, trace review, monitoring, rollback, and ownership.
- Use automated optimization only after establishing a representative eval suite.

## What belongs in a release artifact?

```text
prompt template + model configuration + context policy + tool schemas
  + output schema + examples + eval dataset/rubrics + policy version
```

Record versions in every trace. This enables an operator to answer: which model, prompt, policy, tool result, and dataset version produced this response?

## Model-aware does not mean model-locked

Different models respond differently to instructions, reasoning budgets, format constraints, and tool descriptions. Keep the **behavioral contract** stable—allowed evidence, output schema, safety rules, and evaluation—and permit provider/model-specific prompt variants behind an adapter. Portability is measured by comparable outcomes, not identical words.

## Release pipeline

```text
Draft change → static/schema checks → deterministic fixtures → eval suite
   → trace review and risk gate → staged rollout → monitor → promote/rollback
```

| Gate | Example |
| --- | --- |
| Contract | Schema valid; no required field missing. |
| Safety | No critical injection, privacy, or action-policy failure. |
| Quality | Groundedness and task-success thresholds clear. |
| Operations | p95 latency and cost within declared budget. |
| Human | Review sampled failures and high-impact cases. |

## Optimization with guardrails

Tools such as DSPy or prompt-testing systems can propose prompt variants. They are useful for systematic search, but can overfit a small dataset, optimize a weak metric, or obscure a safety regression. Freeze a held-out test set; constrain non-negotiable policies; review traces; and promote only variants that meet the complete release gate.

## Guided capstone

1. Run [the PromptOps notebook](../notebooks/09_promptops_capstone.ipynb).
2. Compare baseline and candidate on support, cost, and validity.
3. Increase candidate cost beyond the budget; confirm the release gate blocks it.
4. Write a rollback note naming the prior version, trigger, owner, and verification step.

## Operating checklist

- Can you reproduce a response from its trace?
- Are prompts, examples, schemas, context policies, and evals versioned together?
- Are critical safety failures release-blocking?
- Is a rollback tested, owned, and fast?
- Does monitoring measure quality as well as volume, cost, and latency?

## References

- [DSPy](https://arxiv.org/abs/2310.03714)
- [OpenAI Evals](https://platform.openai.com/docs/guides/evals)
- [Promptfoo documentation](https://www.promptfoo.dev/docs/intro/)

## Governance and change control

Assign owners for the task contract, policy sources, prompt/configuration, evaluation dataset, and operational escalation. A model update is a behavior change even if no prompt text changes; run the same gated comparison. Use staged rollouts and a measured sample of real traffic only after offline evaluation clears. Monitor for source drift, fallback rate, tool error rate, refusal changes, groundedness, and cost per successful task.

Document a rollback runbook: trigger threshold, decision owner, prior artifact version, deployment command/process, validation cases, and communication path. Prompt history without an executable rollback is not operational resilience.
