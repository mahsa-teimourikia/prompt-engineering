# 14 — Prompt Evaluation

## Learning objectives

Define task-specific datasets and metrics, compare a baseline and candidate on
identical cases, inspect slices, and make a release decision using safety gates.

## Evaluation loop

![Evaluation Loop Workflow](./diagram-1.svg)

Northstar’s router must classify clear, ambiguous, and missing-evidence cases.
A single demo cannot prove an improvement; ambiguous cases must not be averaged
away by common easy requests.

## Technology landscape and state of the art

**Foundational:** Moving from anecdotal testing ("vibe checks") to rigorous, automated regression testing over frozen datasets.

**Current State of the Art:**
1. **Deterministic Evaluation:** For tasks like classification or extraction, modern pipelines use Structured Outputs (Pydantic) to force LLMs to return strict schemas. This allows developers to write standard unit tests (e.g., `assert response.category == expected_category`) instead of relying on fuzzy string matching.
2. **LLM-as-a-Judge:** For generative or open-ended tasks where deterministic checks fail, the industry uses strong LLMs (like GPT-4o or Gemini 1.5 Pro) to evaluate the outputs of smaller or faster models based on specific rubrics (e.g., tone, helpfulness, hallucination rate).
3. **Continuous Evaluation (PromptOps):** Teams integrate prompt evaluation directly into their CI/CD pipelines. A pull request that changes a prompt must pass a suite of regression tests against a "golden dataset" before merging, preventing silent degradations.
4. **Evaluation Frameworks & Tooling:** The industry has matured to use dedicated evaluation frameworks to automate the execution of Baseline vs. Candidate comparisons across hundreds of test cases. Popular tools include:
   - **Open-source:** [Promptfoo](https://www.promptfoo.dev/) (fast, CLI-based regression testing), [Ragas](https://docs.ragas.io/) (specialized in RAG evaluation metrics), [DeepEval](https://docs.confident-ai.com/docs/getting-started) (Pytest integration for LLMs), and [DSPy](https://github.com/stanfordnlp/dspy) (evaluation-driven prompt compilation).
   - **Enterprise Platforms:** Google Cloud Vertex AI GenAI Evaluation, LangSmith (tracing and evals), and Phoenix by Arize (observability and evals).

## Lab and production

The [notebook](14_prompt_evaluation.ipynb) demonstrates a programmatic evaluation loop comparing a baseline with a candidate prompt on the same frozen set using Pydantic for deterministic accuracy checks. Maintain development, held-out, regression, adversarial, and production feedback sets. Track deterministic validity, support, human review, uncertainty, cost, latency, and confidence intervals where sample size permits. A safety failure is a release blocker, not a number to average away.

## References

- [OpenAI evals guide](https://platform.openai.com/docs/guides/evals)
