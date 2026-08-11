# 29 — AI System Engineering Capstone

## Outcome

Design, evaluate, release, and govern a cross-functional enterprise assistant.
The capstone is not “write a good system prompt”; it is a measurable behavior
system with a business outcome, contracts, evidence, tools, security, human
approval, evaluation, optimization, observability, rollout, rollback, and an
Architecture Decision Record.

## Required deliverables

1. business outcome and risk boundary;
2. task, context, and output contracts;
3. approved evidence and narrow tools;
4. deterministic authorization and human approval;
5. development, held-out, regression, and adversarial evaluations;
6. baseline, measured improvement, and cost/latency decision;
7. versioned behavior artifact, release gate, observability, rollout, and rollback;
8. ADR explaining why simpler and more complex architectures were rejected.

## Lab

The [notebook](ai_system_engineering_capstone.ipynb) checks capstone readiness
against all required components. [lab.py](lab.py) is a transparent completion
gate. A real project must attach actual evidence and test outputs rather than
only filling fields.

## Final principle

Do not ask how to make a prompt sound better. Ask what behavior is needed, how
it is measured, what caused a failure, and what smallest system change improves
it safely.
