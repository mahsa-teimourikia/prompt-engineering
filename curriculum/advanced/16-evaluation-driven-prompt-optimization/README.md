# 16 — Evaluation-Driven Prompt Optimization

## Learning objectives

Classify failures, hypothesize the responsible component, change one variable,
inspect held-out slices, and accept or reject a candidate using quality and
safety gates.

## Optimization loop

    observe failure → classify component → hypothesis → one change → rerun eval
                    → inspect slices → accept or reject

Not every failure is a prompt failure: it may be missing context, an example,
schema, retrieval, tool, model limitation, security boundary, or workflow.

## Lab and production

The [notebook](evaluation_driven_prompt_optimization.ipynb) compares candidates
on a quality/safety gate. [lab.py](lab.py) demonstrates local improvement versus
global regression. Use held-out data, regression plots, change records,
rollbacks, and release gates. Optimization without a trustworthy evaluation
system is meaningless.

## References

- [DSPy optimization overview](https://dspy.ai/learn/optimization/optimizers/)
