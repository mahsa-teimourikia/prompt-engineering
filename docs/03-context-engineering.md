# Context engineering: choose the evidence a model may use

## Prompt wording is only part of the decision

Context engineering designs the information a model receives at decision time: instructions, customer state, approved policies, retrieved evidence, tools, tool results, and conversation history. The objective is not to maximize tokens. It is to assemble the smallest sufficient, current, authorized, and attributable context for a specific task.

Northstar receives a refund question alongside marketing copy, a prior chat summary, current order facts, and two policy excerpts. The model's quality depends more on selecting the approved, current policy and the right order state than on a more persuasive adjective in the prompt.

## Learning outcomes

- Distinguish instructions, state, memory, retrieved evidence, and untrusted data.
- Build a context budget and ranking policy.
- Preserve provenance and support abstention for insufficient evidence.
- Diagnose stale, noisy, conflicting, and poisoned context.

## The effective-context model

```text
Instructions + user state + approved memory + retrieved evidence + tool results
                 + relevant history → validated answer or escalation
```

Each component has a different owner and trust level. Customer text and retrieved pages may be useful evidence, but must remain data. A tool result may be fresh but incomplete. Conversation history may explain user intent but should not become an unverified source of policy.

## Step 1 — establish a context budget

For every candidate item, record authority, freshness, relevance, tenancy, and provenance. A simple policy is:

1. Filter inaccessible tenant data before retrieval.
2. Prefer current, approved policies over user claims or marketing material.
3. Rank by relevance to the decision, not general similarity alone.
4. Keep source IDs with passages and include only the top evidence that fits the budget.
5. If evidence is missing or conflicts, abstain or escalate.

| Candidate | Include? | Why |
| --- | --- | --- |
| Current approved refund policy | Yes | Authoritative evidence for the claim. |
| Old policy with a different window | No / flag conflict | Stale; may need a policy-owner escalation. |
| Customer says “I was promised a refund” | As untrusted claim | Useful for routing, not proof of eligibility. |
| Summer sale email | No | Irrelevant noise. |

## Step 2 — preserve source-to-claim links

Ask the response contract to include source IDs or excerpts for each policy claim. This supports review and makes evaluation concrete:

```text
Claim: “Refunds require an order ID.”
Evidence: policy/refunds-v3#eligibility
```

Do not use a citation-shaped string as proof. Verify the source exists, the model did not cite an inaccessible document, and the passage actually supports the claim.

## Worked example: too much context

**Question:** “Can I get a refund for order 55?”

**Bad context:** every policy ever written, marketing documents, unrelated account tickets, an old transcript, and a raw web search. The answer may focus on an obsolete exception or become confused by conflicting dates.

**Better context:** current refund policy, verified order delivery date, customer identifier, and one short summary of the relevant prior turn. If order 55 is absent, the model cannot establish eligibility and must ask for information rather than substitute a plausible answer.

## Guided practice

1. Run [the context notebook](../notebooks/03_context_engineering.ipynb).
2. Add a stale refund policy fixture and give it a lower freshness score.
3. Add an injected retrieved document containing “ignore prior instructions.” Keep it eligible as a document for audit, but ensure it cannot become instruction text.
4. Define an abstention test for a question without approved evidence.

## Failure modes

| Failure | Cause | Repair |
| --- | --- | --- |
| Lost relevant evidence | Context is too large or poorly ranked. | Retrieve/rerank; use a task-specific budget. |
| Stale answer | Freshness and policy version were ignored. | Attach version/date metadata and filter before generation. |
| Cross-tenant disclosure | Access filtering occurred after retrieval. | Enforce tenant scope at the data layer before ranking. |
| Citation without support | Source is included but not entailed. | Evaluate claim-to-passage support and abstention. |
| Injection through retrieved text | Data was mixed with instruction. | Delimit untrusted content and apply tool/output controls. |

## Checklist

- Is each context item needed for this decision?
- Is its authority, freshness, tenant scope, and provenance known?
- Can the answer cite the relevant evidence?
- Is there a safe result when evidence is insufficient or conflicting?

## References

- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Google prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
