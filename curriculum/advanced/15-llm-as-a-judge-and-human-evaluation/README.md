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
2. **Common Judging Paradigms:**
   - **Absolute Scoring:** Grading a single response against a rubric (e.g., 1 to 5).
   - **Pairwise Comparison (A/B Testing):** Showing the Judge two outputs (Baseline vs. Candidate) and asking it to pick the winner. This often produces more reliable signals than absolute scoring.
   - **Reference-based:** Asking the Judge to compare the generated output against a "gold standard" human answer.
3. **Structured Scoring & Reasoning:** Modern evaluation pipelines use Pydantic to force the Judge to output a structured `{ reasoning: str, score: int }` payload. *Reasoning must always precede the score* (Chain-of-Thought) to improve the judge's accuracy.
4. **Known Biases & Mitigations:** The SOTA actively accounts for **Position Bias** (preferring the first option in pairwise), **Verbosity Bias** (preferring longer answers), and **Self-Enhancement Bias** (models preferring their own generated text). Robust pipelines run permutations (swapping A and B) to mitigate these.
5. **State-of-the-Art Tooling:**
   - **Evaluation Models:** Researchers are creating purpose-built models fine-tuned specifically to act as judges, such as **Prometheus** and **JudgeLM**.
   - **Frameworks:** Tools like **Ragas** (for RAG-specific judging), **Promptfoo**, and **DeepEval** provide out-of-the-box LLM judging metrics.
   - **Human-in-the-Loop (HITL):** LLM Judges are not ground truth. Platforms like **Scale AI**, **Labelbox**, and **Argilla** are used to establish human-labeled baselines. A judge is only considered reliable if its agreement rate with human experts is mathematically verified.

## Lab and production

The [notebook](15_llm_as_a_judge_and_human_evaluation.ipynb) demonstrates a Rubric-Based absolute scoring workflow. It highlights the importance of forcing the Judge to explain its reasoning *before* outputting a final score, and discusses the inherent flaws of LLM Judges (e.g., verbosity bias) that necessitate periodic human evaluation baselines. Judges are evaluators, not ground truth.

## References

- [G-Eval](https://arxiv.org/abs/2303.16634)
