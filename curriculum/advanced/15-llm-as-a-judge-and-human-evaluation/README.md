# 15 — LLM-as-a-Judge and Human Evaluation

## Learning objectives

Compare absolute, pairwise, reference-based, and rubric judging; measure
agreement with human labels; test order and verbosity bias; and define when
deterministic checks or human experts override a judge.

![LLM-as-a-Judge Workflow](./diagram-1.svg)

## Technology landscape and state of the art

**Foundational:** When a model generates open-ended text (like drafting an email), you cannot evaluate it with simple equality checks (`assert actual == expected`).
**Current State of the Art:** 
1. **LLM-as-a-Judge:** The industry standard for evaluating generative tasks at scale is to use a second, often more powerful LLM (the "Judge") to evaluate the output of the first model against a strict rubric.
2. **Structured Scoring:** Modern evaluation pipelines use Pydantic to force the Judge to output a structured `{ score: int, reasoning: str }` payload, which can then be averaged across a dataset to track regression.

## Lab and production

The [notebook](15_llm_as_a_judge_and_human_evaluation.ipynb) demonstrates a Rubric-Based absolute scoring workflow. It highlights the importance of forcing the Judge to explain its reasoning *before* outputting a final score, and discusses the inherent flaws of LLM Judges (e.g., verbosity bias) that necessitate periodic human evaluation baselines. Judges are evaluators, not ground truth.

## References

- [G-Eval](https://arxiv.org/abs/2303.16634)
