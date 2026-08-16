# 04 — Structured Outputs and Typed Interfaces

## Learning objectives

Design a response schema, distinguish JSON syntax from domain correctness,
validate generated data outside the model, and apply bounded repair or a safe
failure path.

## Why this matters

“Return JSON” is not an application interface. Northstar converts a support
request into a case brief for a review queue; it needs known fields, enums,
evidence, and an explicit human-review signal. A model proposes data; the
application decides whether it is valid and authorized.

## Prerequisites and mental model

Complete [Course 02](../02-instruction-contracts/README.md). A contract defines
the decision; a schema turns its proposal into typed data.

![Mental Model Diagram](./diagram-1.svg)

JSON syntax says text parses. Schemas constrain shape. Neither proves that an
answer cites the right policy or makes an allowed claim.

## Worked lab, evaluation, and failures

The [notebook](04_structured_outputs_and_typed_interfaces.ipynb) demonstrates how
native Structured Outputs guarantee syntax and schema validity (preventing malformed
JSON or enum violations entirely). It then focuses on what APIs cannot guarantee:
semantic accuracy and evidence hallucination. It demonstrates an application-side
validation step followed by a bounded-repair loop to fix hallucinated evidence.
Measure semantic, repair, and escalation rates separately; never use unbounded repair loops.

## Technology landscape and state of the art

**Foundational:** strict schema definition, separating syntax validation from semantic validation, and never executing external effects directly from model output.

**Current State of the Art:**
1. **Native Structured Decoding:** Providers (like Google via `response_schema`) now natively guarantee JSON shape by restricting the token generation space. "Output JSON only" prompts are obsolete.
2. **Pydantic Integration:** Modern SDKs map directly to Pydantic models. You define the schema in Python/TypeScript, and the SDK handles the API translation and response deserialization.
3. **Application-Side Semantic Validation:** Because structural constraints do not guarantee factual correctness, state-of-the-art systems heavily rely on deterministic application-side code to verify that the proposed JSON payload matches approved evidence.
4. **Bounded Repair:** If validation fails, the system enters a controlled, short-circuiting repair loop, passing the failure reason back to the model, rather than infinitely retrying.

## Production considerations

Version schemas with prompts and consumers, validate business semantics in code, and authorize effects outside the model. Valid JSON with a false eligibility claim must be rejected.

## References

- [JSON Schema specification](https://json-schema.org/specification)
- [Pydantic documentation](https://docs.pydantic.dev/)
