# 04 — Structured Outputs and Typed Interfaces

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
