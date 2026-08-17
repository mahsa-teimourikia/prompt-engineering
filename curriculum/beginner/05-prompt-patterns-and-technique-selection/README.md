# 05 — Prompt Patterns and Technique Selection

## Learning Objectives
- **Map Failures to Techniques:** Learn to identify a specific observed failure and select the *smallest* prompt technique required to address it.
- **Avoid Pattern Bloat:** Understand the hidden costs (latency, tokens, unreliability) of applying every known prompt technique simultaneously.
- **Measure Justification:** Define the exact metric that justifies the added architectural complexity of a new technique.
- **Establish a Selection Hierarchy:** Master the progression from Direct Instructions -> Schemas -> Few-Shot -> Retrieval -> Agents.

## Core Concepts & Workflow

A technique catalog is useful reference material, not an architecture. Adding deep personas, massive few-shot examples, chain-of-thought reflection, RAG retrieval, and agentic tool-use to every single task creates massive token costs and completely obscures the root causes of failures.

Engineering is about minimizing complexity. You must start with the simplest possible approach (a measurable Instruction Contract). Only when that contract fails—and you can prove it fails against a frozen evaluation suite—do you introduce the next level of complexity to address that specific failure mode.

![Mental Model Diagram](./diagram-1.svg)

## Pattern Map

| Problem | First Technique | Do Not Use It When |
| --- | --- | --- |
| Unclear task | Direct instruction & contract | Evidence is missing from the context |
| Label boundary | Contrastive Few-Shot examples | The direct contract already passes |
| Unreliable interface | Structured Output / Schema | Unstructured prose is explicitly required |
| Missing knowledge | Retrieval (RAG) | The source is untrusted or unauthorized |
| Live bounded data | Tool calling | Deterministic code already has the data |
| Complex subproblems | Planner/Verifier workflow | A simple linear workflow suffices |

## Technology Landscape and State of the Art

**Foundational:** Blindly applying every technique from a blog post (e.g., "always use Chain of Thought") without measuring its impact.

**Current State of the Art:**
1. **Automated Optimization:** The field is moving away from manual "prompt hacking" toward automated compilation. Frameworks like **[DSPy](https://github.com/stanfordnlp/dspy)** treat the prompt as a program, using optimizers to automatically select the best combination of instructions and few-shot examples to maximize a defined metric.
2. **Evaluation-Driven Development:** Teams now spend more time building robust evaluation datasets (using tools like **LangSmith** or **Braintrust**) than writing prompts. A technique is only accepted if the CI/CD pipeline shows a statistically significant improvement on the eval set without regressions.
3. **Compound AI Systems:** Moving from single large prompts to graphs of smaller, specialized calls (e.g., using **[LangGraph](https://langchain-ai.github.io/langgraph/)**). Each node in the graph uses only the minimal techniques required for its specific, narrow sub-task.

## Lab and Production

### The Lab
The [notebook](05_prompt_patterns_and_technique_selection.ipynb) demonstrates the empirical process of technique selection. It establishes a Zero-Shot baseline, measures a specific failure mode (conversational filler), applies a System Instruction to fix it, and then measures the delta. It then observes a second boundary failure and introduces a targeted Few-Shot example to address it, proving the value of incremental technique application.

### Production Best Practices
- **Complexity is a Liability:** Always default to the simplest architecture. (Code > Prompt > Schema > Few-Shot > RAG > Tools > Agents).
- **Rollback Together:** Version the problem statement, the technique choice, the evaluation cases, and the prompt together. If a technique is rolled back, the evaluation expectations must roll back with it.
- **Track Latency Costs:** Every technique (especially Chain-of-Thought or Agents) adds significant latency. Ensure the quality gain justifies the SLA hit.
