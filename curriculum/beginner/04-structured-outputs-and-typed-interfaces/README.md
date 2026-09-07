# 04 — Structured Outputs and Typed Interfaces

**Level:** Beginner · **Estimated time:** 60–90 min · **Prerequisites:** Courses 01–03 and Pydantic validation basics

## Scenario

Northstar converts a customer message into a `CaseBrief` for a review queue.
The model proposes intent, summary, evidence, and an action; the application
decides whether that proposal is structurally valid, semantically supported,
and safe to continue. The replay lab demonstrates that valid JSON can still
cite a fabricated policy, and that a repair loop must have a strict bound.

## Lab walkthrough

- Demonstration 1 parses a valid typed `CaseBrief`.
- Demonstration 2 parses a hallucinated `pol_elite_instant_refund` citation,
  then fails application-side validation with `unknown_evidence_id`.
- Demonstration 3 makes exactly two attempts; the second uses `NONE` and is
  valid.
- Repair-exhausted uses two invalid outputs and returns `None` with terminal
  state `human_review`.
- Demonstration 4 feeds truncated JSON to `parse_structured`; the result has
  `error_code == "not_json"` and raises no exception.

## Exercises

1. Add an approved evidence ID and watch the `unknown_evidence` metric when a
   replay changes from fabricated to approved.
2. Change the repair prompt feedback and watch `repair_attempts` while keeping
   the maximum at two.
3. Add a semantic rule for intent and watch whether the syntax and semantic
   metrics remain separate.

## Checkpoint

1. What does a schema prove? **Shape and types, not factual support or
   authorization.**
2. What should an unknown evidence citation do? **Fail semantic validation
   with `unknown_evidence_id`.**
3. What happens when bounded repair is exhausted? **Return no proposal and
   route to `human_review`.**

## Learning Objectives
- **Enforce Output Shapes:** Transition from parsing raw strings to demanding strict JSON or schema-validated objects.
- **Separate Syntax from Semantics:** Understand that valid JSON syntax does not guarantee factual or business-logic correctness.
- **Implement Application-Side Validation:** Write deterministic code to verify the semantic accuracy of the model's proposed data.
- **Build Bounded Repair Loops:** Design safe retry mechanisms to handle model hallucinations without infinite loops.

## Core Concepts & Workflow

“Return JSON” is not an application interface. If your application expects a case brief containing specific enums, dates, and evidence citations, you cannot rely on a raw string prompt to guarantee that shape. 

A model *proposes* data; the application decides whether it is valid and authorized. Modern systems use native Structured Outputs to guarantee that the syntax (the JSON shape) is 100% correct. However, no API can guarantee that the *content* inside that JSON is factually true or aligns with your business policies. That requires strict, deterministic application-side validation.

![Mental Model Diagram](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Asking the model to "Return JSON", parsing it with `json.loads()`, and hoping it doesn't crash.

**Current State of the Art:**
1. **Native Structured Decoding:** Providers (like Google via `response_schema`) now natively guarantee JSON shape by restricting the token generation space at the API level. "Output JSON only" prompts are obsolete.
2. **Pydantic Integration:** Modern SDKs map directly to **[Pydantic](https://docs.pydantic.dev/)** models. You define the schema in Python/TypeScript, and the SDK handles the API translation and response deserialization entirely.
3. **Application-Side Semantic Validation:** Because structural constraints do not guarantee factual correctness, state-of-the-art systems heavily rely on deterministic application-side code to verify that the proposed JSON payload matches approved evidence.
4. **Bounded Repair:** If validation fails, the system enters a controlled, short-circuiting repair loop, passing the specific failure reason back to the model, rather than infinitely retrying.

## Lab and Production

### The Lab
The [notebook](04_structured_outputs_and_typed_interfaces.ipynb) demonstrates how native Structured Outputs (via the Google GenAI SDK) guarantee syntax validity, preventing malformed JSON entirely. It then highlights the critical gap: semantic hallucination. It implements an application-side validation step followed by a bounded-repair loop to fix hallucinated evidence citations.

### Production Best Practices
- **Version Your Schemas:** Treat your Pydantic schemas like database migrations. Version them alongside your prompts to prevent breaking downstream consumers.
- **Never Execute Directly:** Never execute an external effect (like sending an email or dropping a database table) directly from model output without an application-side authorization gate.
- **Monitor Repair Rates:** Track how often your repair loop is triggered. A high repair rate indicates a flawed prompt or a task that is too complex for the chosen model.

## Further reading

Structured output patterns include prose, JSON mode, schema-constrained
responses, function calls, and grammar-constrained decoding. Select based on
what the next consumer needs: a human may need prose, a program needs a typed
response, and an external capability needs a separately authorized tool
request. Parseable JSON is the weakest guarantee. Schema-valid data adds
required fields and closed values. Semantic validation checks evidence,
relationships, current policy, and domain rules. Authorization and safety
checks remain outside the model. Prefer explicit absence (`NONE`, `null`, a
clarification variant, or escalation) to invented defaults. Keep schemas
small, versioned, and backwards-compatible. Bounded repair should pass the
specific validation error back to the model, cap attempts, record repair
rates, and escalate rather than loop forever.

References: [Pydantic](https://docs.pydantic.dev/),
[JSON Schema](https://json-schema.org/specification),
[OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs),
and [The Prompt Report](https://arxiv.org/abs/2406.06608).
