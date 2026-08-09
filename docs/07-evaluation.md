# Prompt evaluation: improve with evidence

Prompts are code-like artifacts: version them, evaluate them against representative tasks, inspect failures, and gate releases. Build a dataset with normal, ambiguous, adversarial, and regression cases. Measure task-specific correctness and format validity; for grounded work, measure citation support and abstention quality; also record latency and cost.

LLM-as-a-judge can scale a well-defined rubric, but calibrate it against human-reviewed examples and keep deterministic checks for schemas and policy rules. An A/B winner should be chosen on a pre-defined metric, not a memorable demo.

**References:** [OpenAI evals guide](https://platform.openai.com/docs/guides/evals), [G-Eval](https://arxiv.org/abs/2303.16634).
