# 17 — Automatic Prompt Optimization and DSPy

## Learning objectives

Define an objective and dataset split, compare a manual baseline with an
optimized prompt/program, detect overfitting and data leakage, and decide when
optimization cost and portability are justified.

## Lab and production

The [notebook](automatic_prompt_optimization_and_dspy.ipynb) demonstrates an
optimizer that improves a development score while regressing held-out data.
[lab.py](lab.py) is an offline mechanism demo; use DSPy or another optimizer
only behind a reproducible adapter. Automatic optimization without trustworthy
evaluation is meaningless.

## References

- [DSPy optimizers](https://dspy.ai/learn/optimization/optimizers/)
