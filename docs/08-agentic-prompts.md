# Agent and multi-agent prompt contracts

## Design the least autonomous system that works

An agent is not simply a chat response with a role. It is a controlled loop: a goal, state, tools, observations, policy, stopping conditions, and a final result. More autonomy adds latency, cost, observability needs, and risk. Start with a deterministic workflow when the path is known; add a bounded agent only when the system must choose an investigative path.

Northstar can answer a general return-window question with a retrieval workflow. It may need a bounded investigation for “my order is delayed and I was charged twice,” where it must decide which approved read tools to call. A multi-agent team is justified only if specialized analysis makes a measurable improvement over that single-agent baseline.

## Learning outcomes

- Select deterministic workflow, agentic workflow, single agent, or a team based on task uncertainty.
- Specify goal, permitted tools, state, stop rules, budgets, and escalation.
- Define delegation contracts and evidence ownership for a team.
- Evaluate the trajectory as well as the final answer.

## Architecture ladder

| Problem | Preferred design | Why |
| --- | --- | --- |
| Fetch current order status and format it | Deterministic workflow | Steps and tools are known. |
| If late, retrieve policy and draft response | Bounded workflow | One controlled branch and small model decision. |
| Investigate an unclear delivery complaint | Single agent | Tool sequence depends on evidence. |
| Analyze logs, release history, and customer impact | Team only after baseline comparison | Specialization may help, but coordination has cost. |

## A single-agent contract

```text
Goal: prepare an evidence-backed support plan; never execute account actions.
Allowed tools: get_order_status, retrieve_policy, search_tickets.
State: request, evidence, missing information, attempts, recommendation.
Stop: final evidence is sufficient; no permitted tool can reduce uncertainty;
or 3 steps / 4 tool calls / budget threshold is reached.
Escalate: permission failure, conflicting policy, missing critical evidence,
or any proposed consequential action.
```

The stop condition is part of correctness. “Keep investigating until sure” is an unbounded instruction that can create loops and misleading confidence.

## Multi-agent rules

If specialists are used, define ownership rather than merely personas:

```text
Coordinator → gives scope and evidence standard
Order agent → verified order state only
Policy agent → current approved policy only
Analyst → synthesizes claims with source IDs
Risk reviewer → challenges unsupported/actionable recommendation
```

Specify what each role may see, use, produce, and hand off. Shared context should contain minimal verified artifacts, not every private conversation. A coordinator should request evidence and arbitrate conflict; it should not accept a specialist's assertion as a fact.

## Guided practice

1. Run [the agentic prompts notebook](../notebooks/08_agentic_prompts.ipynb).
2. Set the evidence lookup to return nothing; confirm the loop ends with escalation.
3. Add a tool-call budget and record trajectory length.
4. Compare a simple shipping inquiry handled by a workflow with a multi-agent design. What does the extra coordination actually improve?

## Failure modes

| Failure | Control |
| --- | --- |
| Repeated tool calls | explicit step/tool/cost limits and idempotent read tools. |
| Agent takes action based on a draft | separate propose from execute; require authorization and HITL. |
| Specialists debate endlessly | role ownership, message cap, termination condition. |
| Excessive shared context | explicit handoff schema and least-privilege state. |
| Good final answer with wasteful path | evaluate tool arguments, retries, latency, and cost per success. |

## References

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [ReAct](https://arxiv.org/abs/2210.03629)

## Advanced patterns: recovery and durable state

Agent state needs an owner and lifecycle: request-scoped evidence can be discarded after the case; approved customer preference may be stored with consent and expiry; speculative hypotheses should not become durable memory. For long-running work, persist a checkpoint before an approval or external call so the system can resume safely without replaying a write.

Define an explicit handoff schema for teams: objective, scope, allowed sources, evidence IDs, uncertainty, and proposed next step. Compare a team to a single-agent and deterministic baseline on task success, coordination messages, tool calls, latency, and cost. More agents are a cost, not an automatic upgrade.
