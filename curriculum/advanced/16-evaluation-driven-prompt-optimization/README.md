# 16 — Evaluation-Driven Prompt Optimization

## Learning objectives

Classify failures, hypothesize the responsible component, change one variable,
inspect held-out slices, and accept or reject a candidate using quality and
safety gates.

## Optimization loop

![Optimization loop](./diagram-1.svg)

Not every failure is a prompt failure: it may be missing context, an example,
schema, retrieval, tool, model limitation, security boundary, or workflow.

## Technology landscape and state of the art

**Foundational:** Manual prompt engineering by tweaking words and testing on a few examples.
**Current State of the Art:** 
1. **Evaluation-Driven Optimization:** Changing prompts is treated like changing code. You make a hypothesis, change one variable, and run an automated evaluation suite to check for global regressions.
2. **Automatic Prompt Optimization (APO):** Frameworks like DSPy are taking this a step further. Instead of humans tweaking the prompt, you define the evaluation metric and provide a dataset, and the framework uses an LLM to automatically generate, test, and optimize the prompt instructions until the metric is maximized.

## Lab and production

The [notebook](16_evaluation_driven_prompt_optimization.ipynb) compares candidates on a quality/safety gate. It demonstrates the danger of local improvement causing global regression. Use held-out data, regression plots, change records, rollbacks, and release gates. Optimization without a trustworthy evaluation system is meaningless.

## References

- [DSPy optimization overview](https://dspy.ai/learn/optimization/optimizers/)
