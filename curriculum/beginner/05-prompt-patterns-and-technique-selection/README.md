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

    observed failure → hypothesis → smallest technique → frozen evaluation
                     → accept, reject, or choose deterministic software

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

The [notebook](prompt_patterns_and_technique_selection.ipynb) maps observed
failures to techniques, compares their cost/maturity, and rejects a mismatched
solution. Evaluate task success, safety, latency, token use, and regressions;
do not claim a technique is better from one attractive output.

## Production considerations and exercises

Version the problem statement, technique choice, evaluation cases, and rollback
decision together. Tools require application authorization; retrieval requires
source and tenant controls; agent-like planning needs budgets and stop
conditions. Exercises: classify ten failures, justify a deterministic
alternative, and design an evaluation that would disprove your choice.

## References

- [The Prompt Report](https://arxiv.org/abs/2406.06608)
- [ReAct](https://arxiv.org/abs/2210.03629)
