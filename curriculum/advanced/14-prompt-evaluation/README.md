# 14 — Prompt Evaluation

## Learning objectives

Define task-specific datasets and metrics, compare a baseline and candidate on
identical cases, inspect slices, and make a release decision using safety gates.

## Evaluation loop

    dataset → baseline and candidate → deterministic checks → slice analysis
            → human/judge review where needed → release or reject

Northstar’s router must classify clear, ambiguous, and missing-evidence cases.
A single demo cannot prove an improvement; ambiguous cases must not be averaged
away by common easy requests.

## Lab and production

The [notebook](prompt_evaluation.ipynb) compares a baseline with a candidate on
the same frozen set. [lab.py](lab.py) exposes accuracy and failure slices.
Maintain development, held-out, regression, adversarial, and production
feedback sets. Track deterministic validity, support, human review, uncertainty,
cost, latency, and confidence intervals where sample size permits. A safety
failure is a release blocker, not a number to average away.

## References

- [OpenAI evals guide](https://platform.openai.com/docs/guides/evals)
