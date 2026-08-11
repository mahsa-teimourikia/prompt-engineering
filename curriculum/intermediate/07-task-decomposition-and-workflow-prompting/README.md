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

    document → extract typed facts → retrieve/check evidence → draft or clarify

Each stage has an input contract, output contract, bounded retry policy, and
terminal condition. Authorization remains outside the workflow.

## Patterns and evaluation

Compare one large prompt, sequential stages, parallel independent stages, and
an evaluator-optimizer loop. Evaluate task success, supported decisions,
failure isolation, calls, token use, latency, and cost. Use parallelism only
when stages are independent; use an evaluator only if it improves a measured
failure slice.

The [notebook](task_decomposition_and_workflow_prompting.ipynb) compares the
same document through a one-request baseline and an observable workflow.
[lab.py](lab.py) exposes the stage trace.

## Failure modes and production

Avoid hidden state, untyped handoffs, unbounded retries, and workflows that
perform effects directly. Record stage versions and traces, validate each
boundary, make effects idempotent, and stop when evidence is absent. A workflow
should be simpler than an agent when the route is predictable.

## Exercises

Add a missing order ID, an independent parallel classification step, and a
stage-level timeout. Which metric would justify the extra stage?

## References

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
