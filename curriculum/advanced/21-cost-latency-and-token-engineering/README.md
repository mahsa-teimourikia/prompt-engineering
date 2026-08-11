# 21 — Cost, Latency, and Token Engineering

## Learning objectives

Account for instructions, examples, history, retrieval, tools, outputs, and
retries; compare quality/cost/latency alternatives; and reject savings that
break quality or safety gates.

## Lab and production

The [notebook](cost_latency_and_token_engineering.ipynb) compares full, pruned,
and cheap context policies. [lab.py](lab.py) makes the quality gate explicit.
Use token telemetry, caches, context pruning, example selection, output limits,
and model routing only after measuring regressions. Plot Pareto frontiers and
keep safety/evidence checks non-negotiable.

## References

- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting)
