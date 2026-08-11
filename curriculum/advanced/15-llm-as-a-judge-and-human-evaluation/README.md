# 15 — LLM-as-a-Judge and Human Evaluation

## Learning objectives

Compare absolute, pairwise, reference-based, and rubric judging; measure
agreement with human labels; test order and verbosity bias; and define when
deterministic checks or human experts override a judge.

## Lab and production

The [notebook](llm_as_a_judge_and_human_evaluation.ipynb) compares a small human
label set with a judge, then demonstrates why pairwise A/B order must be
randomized. [lab.py](lab.py) is an offline mechanism demonstration, not a claim
about judge quality. Track agreement, disagreement slices, self-preference,
verbosity bias, and calibration. Judges are evaluators, not ground truth.

## References

- [G-Eval](https://arxiv.org/abs/2303.16634)
