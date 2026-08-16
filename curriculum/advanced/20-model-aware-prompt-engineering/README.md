# 20 — Model-Aware Prompt Engineering

## Learning objectives

Keep task contracts portable, isolate model-specific overrides, compare model
classes on the same regression suite, and avoid provider folklore unsupported by
evaluation.

![Portable Prompt Workflow](./diagram-1.svg)

## Technology landscape and state of the art

**Foundational:** Believing "provider folklore" (e.g., adding "take a deep breath" to every prompt because Twitter said it works for GPT-4).
**Current State of the Art:** 
1. **Portable Contracts:** Prompts and schemas should be portable across foundational models. Engineering is done at the contract layer, not by hacking model-specific quirks.
2. **Unified SDK Abstractions:** Frameworks like LiteLLM or the new Google GenAI SDK provide unified interfaces so you can evaluate the exact same prompt against different models.
3. **Data-Driven Model Selection:** You choose between models (e.g., Flash vs. Pro) based on automated evaluation suites measuring correctness, latency, and cost on *your specific prompt contract*, rather than relying on generalized benchmarks.

## Lab and production

The [notebook](20_model_aware_prompt_engineering.ipynb) demonstrates evaluating the exact same Pydantic contract against two different models (`gemini-2.5-flash` and `gemini-2.5-pro`) using the unified Google GenAI SDK. It compares validity, cost (via token counting), and latency to demonstrate how to make data-driven decisions about model selection. Production comparisons should also include instruction following, reasoning, structured output, tool use, multimodality, safety, and version changes.

## References

- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting)
