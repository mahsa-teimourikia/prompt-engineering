# Agent and multi-agent prompt contracts

An agent prompt governs a loop: goal, planning constraints, tools, observations, stopping rules, and escalation. Start with a deterministic workflow when the path is known. Add a bounded agent only when it must choose an investigative path; introduce a team only when specialization measurably improves the result.

Agent roles need explicit ownership, allowed tools, handoff inputs, shared-versus-isolated context, termination conditions, and budget limits. A coordinator should request evidence—not accept unsupported assertions from specialist agents.

**References:** [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [ReAct](https://arxiv.org/abs/2210.03629).
