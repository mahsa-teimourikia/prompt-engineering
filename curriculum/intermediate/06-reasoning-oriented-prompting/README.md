# 06 — Reasoning-Oriented Prompting

## Learning Objectives
- **Implement Chain-of-Thought:** Force models to emit intermediate reasoning steps before generating a final answer.
- **Understand Computation via Tokens:** Grasp why generating more tokens equates to spending more compute cycles on a problem.
- **Enforce Structured Reasoning:** Use Pydantic schemas to strictly separate the `reasoning` payload from the `final_answer`.
- **Evaluate Reasoning Efficacy:** Measure the latency and cost trade-offs of reasoning prompts against the accuracy gains.

## Core Concepts & Workflow

Language models process tokens sequentially. They cannot "think ahead" or quietly deliberate before speaking. If you ask a complex math question and the model immediately outputs "The answer is 42," it has effectively guessed. 

To give a model more "compute time" to solve a problem, you must force it to generate more tokens *before* it outputs the final answer. This is called Chain-of-Thought (CoT) reasoning. By explicitly instructing the model to "think step-by-step" or by enforcing a strict JSON schema where a `reasoning` field must precede the `answer` field, the model can use its own generated logic as context to arrive at the correct conclusion.

![Reasoning Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Adding "think step by step" to the end of a plain-text prompt.

**Current State of the Art:**
1. **Structured Chain-of-Thought:** Modern applications enforce reasoning through strict API schemas (using **[Pydantic](https://docs.pydantic.dev/)**). The model is forced to fulfill a `{ "analysis": "...", "conclusion": "..." }` contract, ensuring the reasoning is parseable and auditable.
2. **Implicit Reasoning Models:** Models like OpenAI's `o1` natively implement hidden Chain-of-Thought generation before returning an answer, trading significant latency for extreme accuracy on complex logical tasks.
3. **Self-Correction & Reflection:** Advanced patterns ask the model to generate a draft, critique its own draft in a separate reasoning block, and then output a final version.

## Lab and Production

### The Lab
The [notebook](06_reasoning_oriented_prompting.ipynb) demonstrates the difference between Zero-Shot answers and Chain-of-Thought answers. It shows how a complex logic puzzle fails when the model is forced to answer immediately, but succeeds when a Pydantic schema forces the model to fill out a `step_by_step_logic` field before outputting the `final_choice`.

### Production Best Practices
- **Reasoning Increases Latency:** Every token generated is time spent. Do not use Chain-of-Thought for simple extraction or classification tasks where latency is critical.
- **Order Matters:** In a JSON schema, the reasoning field *must* be defined before the answer field. If the answer comes first, the model has already committed to a choice and the reasoning will just be a post-hoc justification.
- **Audit the Logs:** The reasoning output is an invaluable debugging tool. Log it to understand *why* a model failed a specific evaluation case.
