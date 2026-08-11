# 18 — Agent and Multi-Agent Prompt Contracts

## Learning objectives

Define agent goals, typed state, narrow tools, permissions, budgets, stop
conditions, handoffs, and escalation; then evaluate trajectories rather than
only final text.

## Lab and production

The [notebook](agent_and_multi_agent_prompt_contracts.ipynb) compares a
deterministic workflow with a supervisor/specialist trajectory. [lab.py](lab.py)
makes tool count and terminal state observable. Extra autonomy must demonstrate
measured benefit. Prompts describe a role; runtime policy enforces identity,
tenant boundaries, authorization, idempotency, and effects.

## References

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
