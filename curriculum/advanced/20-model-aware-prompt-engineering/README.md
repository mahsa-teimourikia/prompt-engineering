# 20 — Model-Aware Prompt Engineering

## Learning objectives

Keep task contracts portable, isolate model-specific overrides, compare model
classes on the same regression suite, and avoid provider folklore unsupported by
evaluation.

## Lab and production

The [notebook](model_aware_prompt_engineering.ipynb) runs a stable contract
through two offline adapters and compares validity, cost, and latency.
[lab.py](lab.py) demonstrates the adapter boundary. Production comparisons also
include instruction following, reasoning, structured output, tool use,
multimodality, context behavior, safety, and version changes.

## References

- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting)
