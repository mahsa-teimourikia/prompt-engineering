# 07 — Task Decomposition and Workflow Prompting

## Learning objectives

Split a task into typed stages only when it improves observability or
reliability, define input/output contracts and terminal conditions, and compare
a single request with a sequential workflow.

## Why this matters

Not every multi-step AI system needs an agent. When the path is known, an
explicit workflow isolates failures, separates deterministic from model-assisted
steps, and makes retries and costs measurable.

## Scenario and mental model

Northstar analyzes a refund document. A single broad request can leap from text
to approval. The workflow extracts an order identifier, checks policy evidence,
and drafts for review.

![Mental Model Diagram](./diagram-1.svg)

Each stage has an input contract, output contract, bounded retry policy, and
terminal condition. Authorization remains outside the workflow.

## Patterns and evaluation

Compare one large prompt, sequential stages, parallel independent stages, and
an evaluator-optimizer loop. Evaluate task success, supported decisions,
failure isolation, calls, token use, latency, and cost. Use parallelism only
when stages are independent; use an evaluator only if it improves a measured
failure slice.

The [notebook](07_task_decomposition_and_workflow_prompting.ipynb) demonstrates
the danger of a "Do Everything" prompt, where the model is asked to read a document,
evaluate policy, and draft a response all at once. It then builds a sequential workflow
using Pydantic to extract facts, a deterministic Python function to check the mock database,
and a final LLM call to draft the response.

## Technology landscape and state of the art

**Foundational:** Building pipelines where LLM outputs are cast into strict types before being passed to deterministic systems or other LLMs.

**Current State of the Art:**
1. **Deterministic Workflows (LangGraph/State Machines):** The industry has realized that not everything needs an autonomous agent. When the sequence of steps is known (e.g., Extract -> Check DB -> Draft), state-of-the-art systems use orchestrators like LangGraph to define a rigid graph where nodes are LLM calls or Python functions, and edges are deterministic. This guarantees predictability.
2. **Autonomous Agents:** Agents should be reserved for scenarios where the *route is unpredictable*. If an LLM is allowed to decide which tool to call and when to finish, that is an Agent. If the route is fixed, it is a Workflow.
3. **Pydantic as the Glue:** Pydantic models are the standard contract between workflow stages. An LLM's output is parsed into a Pydantic object, which serves as the strongly-typed input to the next node in the graph.

## Failure modes and production

Avoid hidden state, untyped handoffs, unbounded retries, and workflows that perform effects directly. Record stage versions and traces, validate each boundary, make effects idempotent, and stop when evidence is absent. A workflow should be simpler than an agent when the route is predictable.

## Exercises

Add a missing order ID, an independent parallel classification step, and a
stage-level timeout. Which metric would justify the extra stage?

## References

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
