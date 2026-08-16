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

![Mental Model Diagram](./diagram-1.svg)

Use observable intermediate artifacts. Do not depend on hidden reasoning traces.

## Patterns, evaluation, and failures

Compare direct answering, decomposition, planner/verifier, self-consistency, and
search only on a frozen suite. Measure supported task success, calls, latency,
tokens, and safe escalation. Failure modes include unsupported assumptions,
unbounded reflection, circular critics, and using an elaborate prompt when a
deterministic check solves the subproblem.

The [notebook](06_reasoning_oriented_prompting.ipynb) uses a technical incident
to demonstrate the evolution of reasoning. It starts with a naive direct prompt that
proposes a restart without checking the logs. It then implements a single-prompt
Chain-of-Thought (forcing the model to emit a `reasoning_steps` array before answering)
which exposes the model's assumptions. Finally, it demonstrates a multi-stage
Planner/Verifier compound system to separate plan generation from evidence verification.

## Technology landscape and state of the art

**Foundational:** Extracting "thinking" into observable, auditable artifacts before taking action.

**Current State of the Art:**
1. **Native Reasoning Models:** We are currently in a massive industry shift. Models like OpenAI's `o1/o3` and Google's `gemini-2.0-flash-thinking-exp` internalize the reasoning loop (Chain-of-Thought) directly into the model's decoding process via Reinforcement Learning. For complex logic puzzles, these models largely deprecate the need for manual "think step by step" prompts.
2. **Compound AI Systems (Agentic Workflows):** While native reasoning models are incredible at logic, they still cannot take autonomous external actions (like reading a database or firing a restart command) safely in a single pass. The state-of-the-art for *action-oriented* reasoning remains a multi-stage Compound System (e.g., Planner -> Tool Executor -> Verifier) built in frameworks like LangGraph or AutoGen.
3. **Structured Reasoning Output:** When using standard models (like `gemini-2.5-flash`), state-of-the-art prompt engineering utilizes Pydantic to enforce a `reasoning_steps` array *before* the `final_answer` field, forcing the model to compute its logic before committing to a token sequence for the answer.

## Production considerations

Bound steps, tool calls, retries, and terminal conditions. Persist only the structured artifacts needed for audit. Treat planner output as a proposal, not authorization.

## Exercises

Add missing evidence, a conflicting symptom, and a deterministic health check.
For each, decide whether the correct fix is prompt, context, workflow, or
application logic.

## References

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [ReAct](https://arxiv.org/abs/2210.03629)
