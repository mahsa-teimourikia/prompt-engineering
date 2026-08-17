# 15 — LLM-as-a-Judge and Human Evaluation

## Learning Objectives
- **Understand Judging Paradigms:** Differentiate between Absolute Scoring, Pairwise Comparison, and Reference-based evaluation techniques.
- **Implement Structured Rubrics:** Build strict grading schemas that force LLM Judges to explain their reasoning before assigning a score.
- **Identify Judge Biases:** Recognize and mitigate systemic flaws in LLM evaluators, such as verbosity, position, and self-enhancement biases.
- **Calibrate with Human Experts:** Establish ground-truth baselines to mathematically verify the reliability of an LLM Judge.

## Core Concepts & Workflow

When a model generates open-ended text—like drafting a customer support email or summarizing a document—you cannot evaluate it with simple equality checks (`assert actual == expected`). 

To evaluate generative tasks at scale, we use a second, often more powerful LLM as a "Judge." This Judge evaluates the output of the first model against a strict qualitative rubric (e.g., tone, helpfulness, hallucination rate). However, Judges are evaluators, not ground truth. They are prone to biases and must periodically be calibrated against Human-in-the-Loop (HITL) expert reviews to ensure alignment.

![LLM-as-a-Judge Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

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

## Lab and Production

### The Lab
The [notebook](15_llm_as_a_judge_and_human_evaluation.ipynb) demonstrates a Rubric-Based absolute scoring workflow. It highlights the critical importance of using Pydantic to force the Judge to output a `reasoning` string *before* an integer `score`, invoking Chain-of-Thought reasoning to improve grading accuracy.

### Production Best Practices
- **Define Overrides:** Clearly define scenarios where deterministic checks (like regex filtering) or human experts immediately override an LLM Judge's decision.
- **Run Permutations:** When doing pairwise judging, always run the evaluation twice, swapping the order of Candidate A and Candidate B to neutralize position bias.
- **Continuous Calibration:** Do not blindly trust the Judge. Sample a small percentage of Judge outputs and route them to human domain experts to calculate an "Agreement Rate" metric over time.

## References
- [G-Eval](https://arxiv.org/abs/2303.16634)
