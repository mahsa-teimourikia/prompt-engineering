# Current coverage map and technique maturity

> This is a guide to the currently published library. The audited target
> sequence and migration status live in the repository-level
> [curriculum evolution plan](../CURRICULUM_EVOLUTION_PLAN.md).

## Storyline

```text
Prompt crafting → prompt engineering → reasoning engineering → context engineering
→ tool and workflow engineering → agent prompt engineering → evaluation-driven
optimization → PromptOps → AI system engineering
```

Every course module answers: what problem it solves, why it may work, when to use it, when not to use it, its cost/complexity, a simpler alternative, and the metric that would prove improvement.

## Maturity labels

| Label | Meaning | Examples in this course |
| --- | --- | --- |
| Foundational | durable mental model or established technique | instruction contracts, examples, schemas, decomposition, evaluation. |
| Practical | commonly useful production pattern | evidence-first RAG, narrow tools, validation, context selection, PromptOps. |
| Emerging | valuable research direction needing measured justification | graph reasoning, automatic prompt optimization, advanced multi-agent search. |
| Legacy/model-dependent | historically important but not universally valuable on current models | ritual zero-shot CoT, blanket persona prompting, unmeasured large few-shot blocks. |

## Canonical learning sequence

1. **Beginner:** LLM behavior; instruction contracts; constraints, examples, and few-shot learning; structured outputs; pattern selection.
2. **Intermediate:** reasoning; task decomposition and workflows; context; conversation and long context; evidence-grounded prompting; tool interfaces; multimodality; security.
3. **Advanced:** evaluation; LLM-as-a-judge and human evaluation; evaluation-driven and automatic optimization; agent contracts; coding agents; model-aware prompting; cost/latency/token engineering.
4. **Production:** PromptOps; observability and incident diagnosis; versioning and release engineering; governance; human-centred AI; portability; architecture selection; capstone.

The present library already supplies strong starting material for LLM behavior, contracts, typed outputs, context, RAG/tools, multimodality, security, evaluation, agents, PromptOps, reasoning, coding agents, efficiency, model awareness, reliability, and optimization. It does not yet make conversation/long context, workflow prompting, tool interfaces, judges, automatic optimization, observability, release engineering, governance, portability, architecture selection, and the capstone first-class complete courses. Those gaps are intentional migration work, not hidden prerequisites.

## Notebook standard

Every practical notebook should include: scenario, objectives, visual model, baseline, improved pattern, credential-free code, experiment, evaluation, failure cases, use/not-use criteria, production considerations, exercise, challenge, takeaway, and references. Provider calls remain optional behind an adapter.
