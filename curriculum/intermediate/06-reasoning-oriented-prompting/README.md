# 06 — Reasoning-Oriented Prompting

## Learning objectives

Decompose a complex task into observable artifacts, compare a direct answer with
a planner/verifier path, and measure task support, calls, latency, and token
cost without requesting private chain-of-thought.

## Why this matters

For a technical incident, an answer can sound decisive while ignoring evidence.
Structured plans, assumptions, subproblem results, and verification outputs make
the process inspectable. They are not automatically better: newer reasoning
models may need less scaffolding, and extra stages add cost and latency.

## Mental model

    request → bounded plan → evidence checks → candidate recommendation
            → verifier → answer, clarification, or escalation

Use observable intermediate artifacts. Do not depend on hidden reasoning traces.

## Patterns, evaluation, and failures

Compare direct answering, decomposition, planner/verifier, self-consistency, and
search only on a frozen suite. Measure supported task success, calls, latency,
tokens, and safe escalation. Failure modes include unsupported assumptions,
unbounded reflection, circular critics, and using an elaborate prompt when a
deterministic check solves the subproblem.

The [notebook](reasoning_oriented_prompting.ipynb) uses a technical incident:
the direct baseline proposes a restart without evidence; the planner/verifier
path exposes an assumption and chooses an evidence-backed escalation. The
transparent implementation is [lab.py](lab.py).

## Production considerations

Bound steps, tool calls, retries, and terminal conditions. Persist only the
structured artifacts needed for audit. Treat planner output as a proposal, not
authorization. Model-specific reasoning controls and verbose prompting are
model-dependent; verify their value on held-out cases.

## Exercises

Add missing evidence, a conflicting symptom, and a deterministic health check.
For each, decide whether the correct fix is prompt, context, workflow, or
application logic.

## References

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [ReAct](https://arxiv.org/abs/2210.03629)
