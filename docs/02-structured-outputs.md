# Examples, constraints, and structured output

## The goal: make an LLM response a dependable interface

Natural-language answers are easy for people to read but difficult for software to route, validate, or measure. Northstar needs to classify a case, show its evidence, and determine whether a specialist must review it. A prose response such as “This looks like a refund issue; probably ask for the order number” is helpful but not a stable interface.

Structured prompting combines two complementary techniques:

1. **Examples** show the decision boundary and style of a task.
2. **A schema** defines the shape that the application can accept.

Examples do not replace requirements. A schema does not prove factual correctness. Together with evaluation they reduce ambiguity and make failures visible.

## Learning outcomes

- Choose when zero-shot instruction is enough and when an example is needed.
- Write varied examples that teach a boundary rather than overfit a happy path.
- Define typed fields, enums, evidence, and safe fallbacks.
- Validate output twice: constrained generation where available, then application code.

## From prose to a contract

| Prose-only response | Structured case brief |
| --- | --- |
| “It may be a refund. Ask for more details.” | `intent: "refund"`, `needs_human: true`, required evidence, and an answer draft. |
| A parser guesses at a heading or bullet. | A validator rejects invalid values before a workflow consumes them. |
| It is hard to count unsupported answers. | Tests can check evidence, allowed intents, and escalation behavior. |

Northstar's minimal contract is:

```json
{
  "intent": "refund | shipping | account | unknown",
  "answer": "customer-facing draft",
  "evidence": ["approved excerpt or source id"],
  "needs_human": true
}
```

The `intent` enum protects routing. The evidence list supports grounding checks. `needs_human` preserves a safe path for incomplete inputs. The application must still check that the evidence actually supports the answer.

## Step 1 — use examples as decision-boundary tests

An effective example shows an input, the relevant evidence, and the desired output. Include contrast:

```text
Input: “Refund my order.”
Evidence: “Refunds require an order ID and are available within 30 days.”
Output: intent=refund; ask for order ID; needs_human=true.

Input: “What is your return window?”
Evidence: same policy
Output: intent=refund; state the policy; needs_human=false.
```

The first example teaches that a request for action is not evidence of eligibility. The second teaches that a general policy question can be answered directly. Add examples for missing evidence, conflicting sources, and out-of-scope questions; do not fill a prompt with near-duplicates.

## Step 2 — constrain the output, then validate it

Use provider-native structured output or JSON Schema when supported. Then perform semantic validation in your own process:

```python
from pydantic import BaseModel
from typing import Literal

class CaseBrief(BaseModel):
    intent: Literal["refund", "shipping", "account", "unknown"]
    answer: str
    evidence: list[str]
    needs_human: bool
```

Schema validation catches a missing `needs_human`, an unknown intent, or an object where a list is expected. It does not detect a fabricated policy citation. Pair it with evidence checks and an evaluation set.

## Repair policy: bounded, observable, and safe

Malformed output is a normal integration failure. A repair loop must be bounded and preserve the original request for audit.

```text
Generate → validate schema
  ├─ valid → run evidence/policy checks → route
  └─ invalid → one bounded repair request containing validation errors
               ├─ valid → route
               └─ invalid → escalate; do not silently coerce
```

Never keep retrying indefinitely. Do not “repair” a forbidden intent into an allowed one without recording the failure.

## Guided practice

1. Open [the notebook](../notebooks/02_structured_outputs.ipynb) and run the deterministic case brief.
2. Add `priority: low | normal | urgent`. Decide which source may set it.
3. Create a malformed response with `intent="payment"`. Confirm that validation rejects it.
4. Add a test for a valid schema whose evidence list is empty. Should it route, clarify, or escalate?

<details><summary>Reasoning guide</summary>

An enum can constrain routing but does not establish business urgency. For a policy answer with no evidence, a grounded assistant should ask for evidence or escalate. Treat an empty list as a semantic failure, not merely valid JSON.

</details>

## Failure modes

| Failure | Repair |
| --- | --- |
| Examples accidentally contain contradictory labels | Version examples and run them against a held-out set. |
| A schema is too permissive | Use enums, minimum lengths, required fields, and domain validators. |
| Model returns valid but unsupported JSON | Check claim-to-evidence relationships separately. |
| Retry loop becomes expensive | Set a retry count, budget, and escalation outcome. |
| Prompt includes private examples | Minimize/redact examples and apply the same data policy as production inputs. |

## Before moving on

- Can a downstream service accept or reject the output without parsing prose?
- Do examples cover both a correct answer and a safe non-answer?
- Is every repair bounded and logged?
- Have you evaluated semantic validity, not only schema validity?

## References

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [The Prompt Report](https://arxiv.org/abs/2406.06608)

## Advanced patterns: choose the right constraint

Use **structured output** when the model must return a data object for your application; use **function calling** when the model must request that your application perform a capability. Do not use either as a replacement for authorization. A useful contract may include a discriminated union: a support assistant either returns an `answer` with evidence or an `escalation` with the missing evidence it needs. This avoids empty fields whose meaning changes case by case.

Keep examples versioned with the schema. When a policy or field changes, update the examples and the dataset together. Run schema-invalid, semantically-invalid, and adversarial samples: valid JSON that includes a fabricated source is a more important test than broken braces.
