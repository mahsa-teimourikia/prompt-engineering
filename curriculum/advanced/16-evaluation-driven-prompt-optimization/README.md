# 16 — Evaluation-Driven Prompt Optimization

## Learning Objectives
- **Treat Prompts as Code:** Move away from trial-and-error tweaking and adopt systematic, version-controlled prompt changes.
- **Hypothesis-Driven Changes:** Isolate variables by changing only one aspect of a prompt (or system) at a time to determine causality.
- **Diagnose Failures Accurately:** Learn to classify whether a failure is caused by the prompt instructions, missing context, flawed schemas, or model limitations.
- **Prevent Global Regressions:** Use automated test suites to ensure that fixing a localized edge case does not break broader system functionality.

## Core Concepts & Workflow

Optimization without a trustworthy evaluation system is meaningless. Before modifying a prompt, you must have a baseline evaluation score. 

When a failure occurs, it is tempting to immediately rewrite the prompt. However, not every failure is an instruction failure: it may be a failure of context retrieval (RAG), a broken tool, a restrictive schema, or a hard model limitation. Optimization requires a scientific approach: classify the failure, form a hypothesis, change *exactly one* variable, and run an automated evaluation suite to check for global regressions across a held-out dataset.

![Optimization loop](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Manual prompt engineering by tweaking words and testing on a few examples.

**Current State of the Art:** 
1. **Evaluation-Driven Optimization:** Changing prompts is treated like changing code. You make a hypothesis, change one variable, and run an automated evaluation suite to check for global regressions. Tools like **[PromptLayer](https://promptlayer.com/)** and **[Langfuse](https://langfuse.com/)** are used to track these iterations and trace evaluation scores back to specific prompt versions.
2. **Automatic Prompt Optimization (APO):** Frameworks like **[DSPy](https://github.com/stanfordnlp/dspy)** are taking this a step further. Instead of humans tweaking the prompt, you define the evaluation metric and provide a dataset, and the framework uses an LLM to automatically generate, test, and optimize the prompt instructions until the metric is maximized.

## Lab and Production

### The Lab
The [notebook](16_evaluation_driven_prompt_optimization.ipynb) guides you through an optimization loop. It explicitly demonstrates the danger of localized improvements—showing how modifying a prompt to fix one specific failing test case can inadvertently lower the overall accuracy of the entire golden dataset.

### Production Best Practices
- **Isolate Variables:** Never rewrite the entire prompt at once. Change one instruction, add one example, or modify one schema field, then evaluate.
- **Held-Out Data:** Do not optimize against your final evaluation dataset, or you will overfit. Use a dedicated development dataset for tweaking, and reserve a held-out test set for final release decisions.
- **Change Management:** Maintain rigorous change records, utilize version control for prompts (PromptOps), and ensure rapid rollback mechanisms are in place if a prompt causes production regressions.
