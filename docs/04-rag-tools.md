# RAG and tool-use prompt interfaces

## Two ways to obtain evidence

Retrieval-augmented generation (RAG) brings curated documents into a response. Tool use queries a system or proposes an action. Both are model interfaces: their names, descriptions, parameters, errors, and results shape model behavior. Both need an application boundary that validates what the model requests and what it receives.

Northstar's support copilot can retrieve a policy excerpt and query verified order status. It cannot issue a refund. That distinction should appear in narrow, typed tools—not in a permissive `admin_api(command)` function.

## Learning outcomes

- Choose RAG for document evidence and a tool for live, structured facts or actions.
- Write tool contracts that make selection and arguments unambiguous.
- Treat retrieved passages and tool results as untrusted data.
- Define error, retry, permission, and escalation behavior.

## A narrow tool contract

```text
get_order_status(order_id: string) → {
  status: "processing" | "shipped" | "delivered" | "not_found",
  last_updated: ISO-8601 date,
  source: string
}
```

This tool says what it can do and what it returns. It does not expose fields the support draft does not need, does not accept arbitrary queries, and does not take action. Validate the order identifier and caller's tenant in code before the tool reaches any system.

## Decision guide

| Need | Design | Example |
| --- | --- | --- |
| Stable policy explanation | RAG/evidence lookup | Current return-window policy. |
| Fresh structured fact | Read-only tool | Current order status. |
| Calculation | Deterministic tool | Delivery-date estimate based on supplied dates. |
| Consequential action | Separate approved workflow | Refund, notification, or account mutation. |
| Missing identifier | Clarifying question | Ask for an order ID before lookup. |

## The evidence-first loop

```text
Classify need → retrieve or call permitted read tool → validate result
  → attach evidence → draft answer → validate output → respond/escalate
```

Avoid “tool call because a tool exists.” Ask whether the call meaningfully reduces uncertainty. A policy question can use an approved excerpt; a specific order claim needs verified status. Track tool calls, arguments, errors, and latency in the trace.

## Error handling is part of the prompt interface

| Result | Model/application behavior |
| --- | --- |
| `not_found` | Ask for a corrected identifier; do not invent account state. |
| timeout | Retry once only if the operation is read-only and budget permits; otherwise escalate. |
| permission denied | Stop and escalate. Never retry with broader authority. |
| malformed result | Reject it, preserve trace, and use a safe fallback. |
| contradictory policy results | Cite conflict and route to a policy owner. |

## Guided practice

1. Run [the RAG and tools notebook](../notebooks/04_rag_and_tools.ipynb).
2. Add a `get_order_status` result with `not_found`; write the expected case brief.
3. Add a `PermissionDenied` fixture; demonstrate that no retry occurs.
4. Compare a narrow policy lookup to an imaginary `admin_api(command)` and list the new attack and reliability risks.

## Safety boundary

Tool descriptions can guide model selection but cannot authorize it. Enforce identity, tenant scope, argument validation, idempotency, rate limits, approval, and audit at the tool/application layer. Treat documents and tool output as data because they may contain malicious or erroneous content.

## References

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Toolformer](https://arxiv.org/abs/2302.04761)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

## Advanced patterns: planning without over-autonomy

For multi-step work, require the system to choose among `answer`, `retrieve`, `read_tool`, `ask_clarifying_question`, and `escalate`. Each option has a precondition: a lookup requires an identifier; an action requires explicit authorization; an answer with a policy claim requires evidence. Capture the proposed tool name and arguments before execution, validate them against session identity and an allowlist, then return a narrow result.

Use idempotency keys and approval gates for any write path. Retrying a read timeout may be reasonable; retrying a payment or notification without an idempotency guarantee can create duplicate harm. Record trajectory quality in evaluation: correct arguments, unnecessary calls, recovery behavior, and forbidden-action rate.
