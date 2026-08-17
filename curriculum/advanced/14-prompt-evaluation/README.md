# 14 — Prompt Evaluation

## Learning Objectives
- **Define Golden Datasets:** Curate frozen, representative datasets that capture production variance and critical edge cases.
- **Establish Baselines:** Calculate deterministic metrics to prove current performance before making changes.
- **Measure Regressions:** Confidently test candidate prompts against baselines using programmatic grading loops rather than anecdotal "vibe checks."
- **Enforce Safety Gates:** Identify failures that represent strict release blockers versus acceptable statistical variance.

## Core Concepts & Workflow

Before changing a prompt, you must know how to measure the impact of that change. Anecdotal testing on a few manual examples is dangerous because fixing one edge case often breaks another (regression). 

The Evaluation Loop solves this by running every candidate prompt against a "Golden Dataset" of frozen test cases. Northstar’s router must accurately classify clear, ambiguous, and missing-evidence cases. A single successful demo cannot prove a prompt is an improvement; ambiguous cases must not be averaged away by a high volume of easy requests.

![Evaluation Loop Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Moving from anecdotal testing ("vibe checks") to rigorous, automated regression testing over frozen datasets.

**Current State of the Art:**
1. **Deterministic Evaluation:** For tasks like classification or extraction, modern pipelines use Structured Outputs (Pydantic) to force LLMs to return strict schemas. This allows developers to write standard unit tests (e.g., `assert response.category == expected_category`) instead of relying on fuzzy string matching.
2. **LLM-as-a-Judge:** For generative or open-ended tasks where deterministic checks fail, the industry uses strong LLMs (like GPT-4o or Gemini 1.5 Pro) to evaluate the outputs of smaller or faster models based on specific rubrics (e.g., tone, helpfulness, hallucination rate).
3. **Continuous Evaluation (PromptOps):** Teams integrate prompt evaluation directly into their CI/CD pipelines. A pull request that changes a prompt must pass a suite of regression tests against a "golden dataset" before merging, preventing silent degradations.
4. **Evaluation Frameworks & Tooling:** The industry has matured to use dedicated evaluation frameworks to automate the execution of Baseline vs. Candidate comparisons across hundreds of test cases. Popular tools include:
   - **Open-source:** [Promptfoo](https://www.promptfoo.dev/) (fast, CLI-based regression testing), [Ragas](https://docs.ragas.io/) (specialized in RAG evaluation metrics), [DeepEval](https://docs.confident-ai.com/docs/getting-started) (Pytest integration for LLMs), and [DSPy](https://github.com/stanfordnlp/dspy) (evaluation-driven prompt compilation).
   - **Enterprise Platforms:** Google Cloud Vertex AI GenAI Evaluation, LangSmith (tracing and evals), and Phoenix by Arize (observability and evals).

## Lab and Production

### The Lab
The [notebook](14_prompt_evaluation.ipynb) demonstrates a programmatic evaluation loop comparing a baseline with a candidate prompt on the same frozen set. It uses Pydantic schemas to enforce deterministic accuracy checks (exact match routing). It then demonstrates a generative evaluation scenario utilizing LLM-as-a-Judge with a strict Pydantic grading rubric.

### Production Best Practices
- **Dataset Stratification:** Maintain distinct datasets for development, held-out validation, regression tracking, adversarial attacks, and production feedback.
- **Track Comprehensive Metrics:** Go beyond accuracy. Track deterministic validity, support alignment, human review scores, uncertainty bounds, cost (token usage), and latency.
- **Strict Release Gates:** A safety failure (e.g., executing a destructive command) is a hard release blocker, not merely a number to be averaged out by a high overall accuracy score.

## References
- [OpenAI evals guide](https://platform.openai.com/docs/guides/evals)
