# 05 — Prompt Patterns and Technique Selection

## Learning objectives

Identify an observed failure, select the smallest technique that addresses it,
state when not to use that technique, and define the metric that would justify
its added complexity.

## Why this matters

A technique catalog is useful reference material, not an architecture. Adding
persona text, examples, reflection, retrieval, tools, and agents to every task
creates cost and hides failure causes. Start with a measurable contract and add
only the component that resolves a demonstrated gap.

## Mental model

![Mental Model Diagram](./diagram-1.svg)

## Pattern map

| Problem | First technique | Do not use it when |
| --- | --- | --- |
| Unclear task | direct instruction and contract | evidence is missing |
| Label boundary | contrastive examples | the direct contract already passes |
| Unreliable interface | schema constraint | unstructured prose is required |
| Missing current knowledge | retrieval context | source is untrusted or unauthorized |
| Live bounded data | tool calling | deterministic code already has the data |
| Complex subproblems | planner/verifier workflow | a simple workflow works |

Direct instructions, schemas, and validation are foundational. Few-shot
boundaries, retrieval, and narrow tools are practical. Persona rituals, verbose
reasoning requests, and elaborate reflection loops are model-dependent: test
them, do not assume they help. Automatic optimization and learned context
policies are emerging and require held-out evaluation.

## Worked lab and evaluation

The [notebook](05_prompt_patterns_and_technique_selection.ipynb) demonstrates the
empirical process of technique selection using an entity extraction scenario. It establishes
a Zero-Shot baseline, measures a specific failure mode (conversational filler), applies
a System Instruction to fix it, and then measures the delta. It then observes a second boundary
failure and introduces a Few-Shot example to address it, proving the value of incremental
technique application over blindly applying all patterns at once.

## Technology landscape and state of the art

**Foundational:** Measuring failures against a frozen evaluation suite before applying any prompt engineering technique.

**Current State of the Art:**
1. **Automated Optimization (DSPy):** The field is moving away from manual "prompt hacking" toward automated compilation. Frameworks like DSPy treat the prompt as a program, using optimizers to automatically select the best combination of instructions and few-shot examples to maximize a defined metric over a training set.
2. **Evaluation-Driven Development:** Teams now spend more time building robust evaluation datasets (using tools like LangSmith or Braintrust) than writing prompts. A technique is only accepted if the CI/CD pipeline shows a statistically significant improvement on the eval set without regressions.
3. **Compound AI Systems:** Moving from single large prompts to graphs of smaller, specialized calls (e.g., using LangGraph or custom routing). Each node in the graph uses only the minimal techniques required for its specific sub-task.

## Production considerations and exercises

Version the problem statement, technique choice, evaluation cases, and rollback decision together. Tools require application authorization; retrieval requires source and tenant controls; agent-like planning needs budgets and stop conditions. Exercises: classify ten failures, justify a deterministic alternative, and design an evaluation that would disprove your choice.

## References

- [The Prompt Report](https://arxiv.org/abs/2406.06608)
- [ReAct](https://arxiv.org/abs/2210.03629)
