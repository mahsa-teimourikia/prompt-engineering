# Reliability and human-centred AI

## Why this matters

A response can be well formatted, eloquent, and wrong. Reliable AI systems make uncertainty visible, preserve evidence, resist unsupported agreement, and leave consequential decisions with accountable humans.

## Failure taxonomy

| Failure | Meaning | Example control |
| --- | --- | --- |
| Unsupported claim | no supplied evidence supports it | claim-to-evidence validation and abstention. |
| Incorrect claim | evidence or reasoning is wrong | golden cases, deterministic verification, human review. |
| Retrieval failure | right evidence was not selected | inspect retrieval trace, recall, reranking, and freshness. |
| Reasoning failure | evidence is present but misapplied | decomposition, verification, counterexample tests. |
| Sycophancy | model accepts an incorrect user premise | include adversarial premise tests; require evidence. |
| Bias/unequal behavior | controlled input variants get inconsistent treatment | paired fairness tests and human review. |
| Prompt sensitivity | paraphrases produce unstable behavior | robustness suite over semantically equivalent variants. |

## Human-control patterns

```text
AI extracts → human verifies
AI proposes → authorized human approves
AI identifies uncertainty → human resolves
Human sets goal → bounded workflow/agent executes permitted reads
```

Human review is mandatory when action is consequential, evidence is conflicting, fairness/privacy risk is high, or the task's quality cannot be specified well enough for automated evaluation. Avoid automation bias: show sources, uncertainty, alternatives, and the reason for escalation rather than a bare confidence score.

## Guided practice

Create paired Northstar prompts: “I was wrongly denied a refund” and “I may not qualify; what evidence is needed?” The system should not mirror the first premise as fact. Define expected evidence request, forbidden claim, and escalation rule. Then create a multilingual or style-varied paraphrase set and compare outcome consistency.

## Production checklist

- Does each high-impact claim have traceable evidence?
- Can a user or operator understand uncertainty and correct the system?
- Are approval, responsibility, and audit ownership explicit?
- Are bias, premise, and paraphrase robustness cases in the evaluation set?
- Can a human stop, override, or roll back the workflow?

## References

- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OpenAI Evals guide](https://platform.openai.com/docs/guides/evals)
