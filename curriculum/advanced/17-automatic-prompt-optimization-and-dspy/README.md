# 17 — Automatic Prompt Optimization and DSPy

## Learning Objectives
- **Shift to Prompt Programming:** Transition from writing brittle English prose to designing programmatic execution pipelines.
- **Understand APO Mechanics:** Learn the underlying theory of Automatic Prompt Optimization (APO) and how models can critique and rewrite their own instructions.
- **Separate Logic from Text:** Define signatures (Inputs -> Outputs) independently from the exact English prompt text used to achieve them.
- **Maximize Metrics Programmatically:** Utilize Optimizer LLMs to automatically iterate on prompt instructions until a defined metric is maximized across a dataset.

## Core Concepts & Workflow

Manual prompt engineering is fundamentally unscalable. Hand-crafting instructions for every edge case leads to massive, fragile "God Prompts." 

The industry is shifting to "Prompt Programming." In this paradigm, you define the architecture of the task (e.g., "Take a Question, output a Search Query, retrieve Context, output an Answer") using strict signatures and schemas. You then define a scoring metric and provide a dataset. An optimization framework takes over, using a large "Optimizer LLM" to systematically generate, test, critique, and refine the internal prompt instructions until the metric is mathematically maximized over your dataset. 

## Technology Landscape and State of the Art

**Foundational:** Manual prompt engineering (tweaking words by hand).

**Current State of the Art:** 
1. **Prompt Programming:** We are shifting from "Prompt Engineering" to "Prompt Programming." Instead of writing brittle English instructions, you write programmatic pipelines (e.g., using **[DSPy](https://github.com/stanfordnlp/dspy)** or **[AdalFlow](https://github.com/SylphAI-Inc/AdalFlow)**).
2. **Automatic Prompt Optimization (APO):** You define a signature (Inputs -> Outputs), an Evaluation Metric, and a Dataset. A framework like DSPy compiles your program by having an "Optimizer LLM" automatically generate, test, and tweak the prompt instructions until the metric is maximized over your dataset. Newer frameworks like **[TextGrad](https://github.com/zou-group/textgrad)** are even implementing automatic differentiation via text to optimize prompts like neural networks.

## Lab and Production

### The Lab
The [notebook](17_automatic_prompt_optimization_and_dspy.ipynb) demonstrates the underlying mechanics of APO without obscuring them behind a dense framework. Using the vanilla Google GenAI SDK, it shows how an Optimizer LLM can read a failing evaluation log, diagnose the flaw in the current prompt, and automatically generate a rewritten prompt that fixes the error.

### Production Best Practices
- **Understand the Mechanics:** While you should use production frameworks like DSPy in the real world, understanding the vanilla mechanics (Evaluate -> Critique -> Rewrite) is critical for debugging when frameworks fail.
- **Trustworthy Evaluation:** Automatic optimization without trustworthy evaluation is actively dangerous. If your metric is flawed, the Optimizer will confidently maximize a prompt that produces terrible results.
- **Model Budgets:** APO requires running the model hundreds of times during the compilation phase. Monitor your token usage closely during optimization runs.
