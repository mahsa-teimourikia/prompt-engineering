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

    candidate → JSON parse → schema validation → semantic/evidence validation
              → queue, bounded repair, clarification, or escalation

JSON syntax says text parses. Schemas constrain shape. Neither proves that an
answer cites the right policy or makes an allowed claim.

## Worked lab, evaluation, and failures

The notebook tests a valid response, malformed JSON, enum violation, unexpected
field, and schema-valid unsupported claim. It then repairs an extra-field
response once. Measure parse, schema, semantic, repair, and escalation rates
separately; never use unbounded repair loops.

## Production considerations

Use JSON Schema or Pydantic-style models, version schemas with prompts and
consumers, validate business semantics in code, and authorize effects outside
the model. Valid JSON with a false eligibility claim must be rejected.

## References

- [JSON Schema specification](https://json-schema.org/specification)
- [Pydantic documentation](https://docs.pydantic.dev/)
