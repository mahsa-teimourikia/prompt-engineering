# Course coverage map and technique maturity

## Storyline

```text
Prompt crafting → prompt engineering → reasoning engineering → context engineering
→ knowledge/RAG → tools/workflows → agents → evaluation → PromptOps
```

Every course module answers: what problem it solves, why it may work, when to use it, when not to use it, its cost/complexity, a simpler alternative, and the metric that would prove improvement.

## Maturity labels

| Label | Meaning | Examples in this course |
| --- | --- | --- |
| Foundational | durable mental model or established technique | instruction contracts, examples, schemas, decomposition, evaluation. |
| Practical | commonly useful production pattern | evidence-first RAG, narrow tools, validation, context selection, PromptOps. |
| Emerging | valuable research direction needing measured justification | graph reasoning, automatic prompt optimization, advanced multi-agent search. |
| Legacy/model-dependent | historically important but not universally valuable on current models | ritual zero-shot CoT, blanket persona prompting, unmeasured large few-shot blocks. |

## Learning sequence

1. [LLM behavior and prompt structure](18-llm-behavior-and-prompt-structure.md) and [instruction contracts](01-instruction-contracts.md)
2. [Structured output and examples](02-structured-outputs.md), then [technique catalog](14-technique-catalog.md)
3. [Reasoning techniques](11-reasoning-techniques.md), [context engineering](03-context-engineering.md), and [RAG/tools](04-rag-tools.md)
4. [Multimodality](05-multimodal.md), [security](06-prompt-security.md), and [reliability/human-centred AI](19-reliability-and-human-centred-ai.md)
5. [Evaluation](07-evaluation.md), [agents](08-agentic-prompts.md), [PromptOps](09-promptops.md), and [cost/latency](13-cost-latency-engineering.md)

## Notebook standard

Every practical notebook should include: scenario, objectives, visual model, baseline, improved pattern, credential-free code, experiment, evaluation, failure cases, use/not-use criteria, production considerations, exercise, challenge, takeaway, and references. Provider calls remain optional behind an adapter.
