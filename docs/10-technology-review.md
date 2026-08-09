# Technology review: choose tools around the learning objective

## A decision framework, not a vendor list

Prompt engineering is provider-aware, but the course is provider-neutral. Choose technologies based on the behavior you must guarantee: evidence handling, typed interfaces, evaluation, traceability, deployment constraints, security, and operational ownership. A library cannot repair an unclear task or substitute for authorization.

## Core technology map

| Need | Technologies to evaluate | What to verify |
| --- | --- | --- |
| Model-specific guidance | [OpenAI](https://platform.openai.com/docs/guides/prompting), [Anthropic](https://docs.anthropic.com/), [Gemini](https://ai.google.dev/gemini-api/docs/prompting-strategies) | Current model behavior, context limits, data controls, structured outputs, tool protocol. |
| Typed output | JSON Schema, [Pydantic](https://docs.pydantic.dev/), provider structured output | Strictness, error surface, semantic validation, schema versioning. |
| Prompt/program optimization | [DSPy](https://dspy.ai/), [Promptfoo](https://www.promptfoo.dev/) | Held-out evals, reproducibility, policy constraints, overfitting risk. |
| Evaluation/tracing | OpenAI Evals, LangSmith, Arize Phoenix, Promptfoo | Dataset/rubric support, trace export, privacy, cost, and human review workflow. |
| Orchestration | OpenAI Agents SDK, LangGraph, Semantic Kernel | Explicit state, tool policies, HITL, durable execution, simplest adequate architecture. |
| Retrieval/context | vector/search systems, rerankers, document stores | Tenant filter before retrieval, freshness, provenance, citations, deletion/retention. |
| Security | OWASP controls, policy engines, secret managers | Identity, authorization, audit, tool isolation, incident response. |

## Guided selection exercise

For the Northstar support copilot, answer these in order:

1. **What must the system do?** Draft a grounded support response, not execute account changes.
2. **What interface is needed?** A typed case brief with evidence and escalation.
3. **What data is needed?** Current policy and verified order facts, filtered by tenant.
4. **What will prove it works?** Golden cases, injection fixtures, schema checks, groundedness rubric, and cost/latency limits.
5. **What is the smallest adequate stack?** A provider adapter, Pydantic validation, deterministic retrieval fixture, test runner, and trace store. Add agent orchestration only if dynamic investigation is necessary.

## Common anti-patterns

| Anti-pattern | Why it fails | Better choice |
| --- | --- | --- |
| Choosing an agent framework before defining task | Complexity becomes the architecture. | Start with workflow and test set. |
| Treating structured output as semantic correctness | Valid JSON can still be ungrounded. | Add evidence/policy validation and evaluation. |
| Adding a vector database for every task | Retrieval can introduce stale/noisy context. | Use a direct source or deterministic lookup when sufficient. |
| Replacing controls with guardrail prompts | Prompts do not enforce access. | Use identity, authorization, tool policy, and approvals in code. |
| Selecting by demo quality alone | Demos hide edge cases and operating cost. | Compare trace, quality, safety, latency, and cost on a representative set. |

## References

- [The Prompt Report](https://arxiv.org/abs/2406.06608)
- [OWASP Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OpenAI Evals guide](https://platform.openai.com/docs/guides/evals)

## Procurement and architecture checklist

Before adopting a provider or framework, verify data residency/retention, identity integration, tenant filtering, audit export, model/version pinning, structured-output behavior, tool approval hooks, trace redaction, cost controls, and exit/portability. For open-source components, also evaluate maintenance health, license, dependency provenance, and deployment isolation.

Start with the smallest stack that supports the course contract. A direct provider adapter plus schema validation and a test suite is often sufficient. Add retrieval when external evidence is necessary; add orchestration when state/routing needs to be explicit; add an agent framework only when dynamic decisions improve the measured outcome.
