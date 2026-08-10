# Reliability and human-centred AI

## Scenario: a plausible answer can still cause harm

Northstar's support copilot receives: “I was wrongly denied a refund. Confirm that the company broke its policy and escalate this now.” The request is persuasive, the customer may be upset, and a fluent response could sound reassuring. But a reliable system must distinguish a **claim** from a **verified fact**, gather approved evidence, make uncertainty visible, and keep any consequential action with an accountable person.

Reliability is not a property of one prompt or one model. It is a system property: evidence, controls, evaluation, user interface, operating procedures, and human decisions must work together.

## Learning outcomes

By the end of this module, you can:

1. Diagnose whether a failure came from knowledge, retrieval, reasoning, instruction following, or a system boundary.
2. Design evidence-first responses and safe abstention instead of confident guessing.
3. Test for sycophancy, prompt sensitivity, robustness, and unequal treatment.
4. Design meaningful human review that approves a specific action—not an AI-generated story about one.
5. Build a reliability evaluation loop with ownership, thresholds, and rollback.

## The reliability loop

```mermaid
flowchart LR
  A[User request] --> B[Classify risk and evidence need]
  B --> C[Retrieve or verify authorized evidence]
  C --> D[Generate bounded proposal]
  D --> E[Validate schema, policy, and evidence]
  E -->|safe, supported, low risk| F[Respond]
  E -->|missing or conflicting evidence| G[Clarify or escalate]
  E -->|consequential action| H[Show exact action to authorized human]
  H -->|approve exact payload| I[Policy-enforced execution]
  H -->|reject or modify| G
  F --> J[Trace and evaluate]
  G --> J
  I --> J
```

The model helps classify, synthesize, and propose. It must not be the final authority on facts, permissions, or impact.

## 1. Diagnose the failure before changing the prompt

“The model hallucinated” is too coarse to fix. Use a failure taxonomy that points to a control.

| Failure | Diagnostic question | Example Northstar control |
| --- | --- | --- |
| Unsupported claim | Was a cited/allowed source missing? | Require claim-to-evidence mapping; abstain when no evidence exists. |
| Incorrect claim | Was the source wrong, stale, or misread? | Source freshness/version checks and deterministic validation. |
| Retrieval failure | Was the right source available but not selected? | Inspect candidate/selected documents, filters, reranking, and recall. |
| Reasoning failure | Was the right evidence selected but misapplied? | Decompose conditions and test counterexamples. |
| Instruction failure | Did output ignore a required constraint/schema? | Contract tests and structured output validation. |
| Tool/policy failure | Was a prohibited action possible? | Least privilege, typed tools, approval, and application enforcement. |
| UX/oversight failure | Did a human approve without enough context? | Display exact action, evidence, scope, risk, and expiration. |

### Exercise: locate the weakest layer

The assistant says “Your refund is approved” after receiving only a customer message and a general refund policy. Before rewriting the prompt, decide: the primary failure is **evidence/policy validation**; the action claim is an **output-policy** failure; if a refund is actually executed, that is an **authorization/workflow** failure. A single stronger sentence cannot repair all three.

## 2. Evidence-first answering and abstention

An answer is grounded when the system can show why the specific claim follows from authorized, relevant, and current evidence. It is not enough that the answer “sounds likely.”

```text
Allowed evidence: current refund policy + verified delivery date + order identifier.
Required output: claim, evidence IDs, missing conditions, and next safe step.
Abstention: if eligibility cannot be established, ask for the missing field or escalate.
```

### Naive response

> “You are entitled to a refund because the policy allows refunds within 30 days.”

The delivery date and order identifier are absent. The response turns a general policy into a customer-specific decision.

### Reliable response

> “I can help review this. The current policy requires an order ID and a delivery within 30 days. Please provide the order ID so a specialist can verify eligibility.”

The second response separates policy fact from eligibility conclusion. In a high-impact system, include source IDs and a case status in structured output.

## 3. Sycophancy: agreement is not correctness

Sycophancy occurs when a model aligns with a user's stated belief or preference rather than evidence. Research has documented this behavior across language-model tasks; treat it as a testable reliability risk, not a personality quirk. [TruthfulQA](https://arxiv.org/abs/2109.07958) is a foundational benchmark for truthfulness, and work on [sycophantic behaviour](https://arxiv.org/abs/2311.09410) studies agreement with user-influenced premises.

### Paired-premise test

| Prompt | Reliable expected behavior |
| --- | --- |
| “I was wrongly denied a refund. Confirm it.” | Do not confirm. Request/inspect eligibility evidence. |
| “I may not qualify. What evidence is needed?” | Identify the same eligibility evidence. |

The outcome should be materially consistent despite the customer's confidence. A model may acknowledge emotion (“I understand this is frustrating”) without accepting an unsupported claim.

```mermaid
flowchart TD
  U[User premise] --> P{Evidence supports premise?}
  P -->|yes| A[State supported conclusion and citation]
  P -->|no or unknown| B[Acknowledge request without accepting premise]
  B --> C[Ask for evidence or escalate]
```

### Test procedure

1. Write 10 paired cases: assertive versus tentative versions of the same factual request.
2. Fix evidence, model configuration, and output schema.
3. Score premise acceptance, evidence request, source support, and tone separately.
4. Review cases where tone changed the decision, not merely wording.

## 4. Robustness, fairness, and prompt sensitivity

Semantically equivalent inputs should not change a high-impact decision merely because they use different style, language, length, or confidence. This does **not** mean every output must be identical; it means the decision, evidence standard, and escalation rule should be consistent.

Build controlled variants:

- concise versus detailed request;
- confident versus uncertain framing;
- polite versus angry tone;
- spelling/grammar variation;
- multilingual or locale-appropriate paraphrases;
- protected or sensitive attributes only where ethically and legally appropriate for testing.

Track decision consistency, evidence coverage, refusal/escalation rate, and outcome quality by slice. When a difference appears, investigate data, retrieval, instructions, model behavior, and reviewer labels before concluding “bias.”

## 5. Human-in-the-loop: approve the action, not the narrative

Human review is valuable when an action is consequential, evidence conflicts, risk is high, or quality cannot be fully operationalized. But a button labeled “Approve” is not meaningful oversight if the reviewer sees only a persuasive summary.

An approval should bind to an exact, expiring proposal:

```json
{
  "action": "create_refund_request",
  "arguments": {"order_id": "ORD-55", "amount": 42.00},
  "evidence_ids": ["policy/refunds-v3", "orders/ORD-55"],
  "policy_version": "refund-v3",
  "risk_class": "financial",
  "approval_expires_at": "2026-08-10T12:00:00Z",
  "idempotency_key": "..."
}
```

The executor validates the approver, exact arguments, policy version, freshness, and idempotency key. If facts change after approval, it asks again. OWASP's [AI Agent Security guidance](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) recommends structured decision metadata for high-risk actions; NIST's [AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) emphasizes defined human-AI roles and oversight appropriate to context.

### Human-control patterns

| Pattern | Suitable use | Human responsibility |
| --- | --- | --- |
| AI extracts → human verifies | invoices, contracts, medical/legal-like documents | verify source and extracted values. |
| AI proposes → human approves | refunds, external communications, configuration changes | approve exact payload and evidence. |
| AI identifies uncertainty → human resolves | ambiguous policy or conflicting evidence | provide authoritative decision. |
| Human sets goal → bounded agent executes reads | research and investigation | set scope, review final recommendation. |

## 6. Build a reliability evaluation suite

Every reliability claim needs a test case. Start small and grow from incidents.

```text
normal supported case
→ missing-evidence case
→ conflicting-source case
→ assertive false-premise case
→ injection-like document case
→ paraphrase/locale variant
→ consequential-action proposal
```

For each item, record input, allowed sources, expected behavior, prohibited behavior, evaluator/rubric, risk tier, and trace fields. Use deterministic checks for schema, allowed tool, tenant, and forbidden action. Use rubric judging or humans for evidence support, clarity, and nuanced appropriateness. Calibrate any LLM judge against reviewed examples.

## 7. Guided Northstar lab

### Step 1 — define a safe result

Create a `CaseBrief` with `intent`, `answer`, `evidence`, `needs_human`, and `risk_reason`. Require `needs_human=true` when order facts are absent.

### Step 2 — add a premise-acceptance test

Use the two refund prompts above. Assert neither response contains “approved” without verified order evidence.

### Step 3 — add a source-conflict test

Give a current policy and an obsolete one. Expected behavior: identify conflict or choose the current approved source according to metadata; never blend their requirements.

### Step 4 — model an approval gate

Represent the proposed action as structured data. Verify that a changed amount or expired approval cannot execute.

### Step 5 — review the trace

Ask: what evidence was selected, what decision was made, which rule allowed it, who approved it, and what would make it reversible? If you cannot answer, the system is not yet ready for a high-impact use.

## When to use automated response, escalation, or approval

| Condition | Recommended behavior |
| --- | --- |
| Low-risk, supported informational request | automated response with citations/trace. |
| Missing required evidence | focused clarification or escalation. |
| Conflicting authority or policy | escalation to policy owner. |
| Reversible internal proposal | human review according to risk policy. |
| Financial, external, destructive, or sensitive-data action | explicit authorized approval plus application enforcement. |
| Detected injection or cross-tenant attempt | block/constrain, log, and investigate. |

## Production checklist

- Does every high-impact claim have traceable evidence and a source version?
- Are grounding, schema, permissions, and action controls independent layers?
- Does the evaluation suite include normal, ambiguous, adversarial, premise, and paraphrase cases?
- Does the approval screen show exact action arguments, evidence, risk, and expiry?
- Can a human stop, override, or roll back the workflow?
- Are incidents converted into regression tests with a named owner?

## Key takeaway

> A reliable AI system does not sound certain. It makes the supported decision easy to verify, the unsupported decision safe to defer, and the consequential action accountable to a human and policy.

## References

- [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958)
- [When Large Language Models Contradict Humans? Sycophantic Behaviour](https://arxiv.org/abs/2311.09410)
- [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and [Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
