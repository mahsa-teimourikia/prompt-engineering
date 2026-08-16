# 23 — Prompt Observability and Failure Diagnosis

## Learning objectives

Trace behavior artifacts, model/configuration, context, examples, tools,
validation, evaluation, tokens, latency, and cost; then isolate deliberate
regressions without exposing sensitive content or private reasoning.

![Observability Tracing](./diagram-1.svg)

## Technology landscape and state of the art

**Foundational:** Blindly guessing why a prompt failed, or manually writing `print()` statements to read massive prompt payloads in production logs.
**Current State of the Art:** 
1. **OpenTelemetry Semantics:** LLM calls are now instrumented using OpenTelemetry spans. A single "Trace" captures the entire lifecycle of a request, breaking it down into spans like `Retrieve Context` and `LLM Generation`.
2. **Dedicated LLM Observability Platforms:** Tools like LangSmith, Phoenix, Datadog LLM Observability, and Vertex AI allow engineers to visually inspect these traces, filtering by latency, token cost, or user feedback (e.g., thumbs down).
3. **Privacy and PII Scrubbing:** In enterprise environments, you cannot simply log the full prompt to a database, as it may contain Personally Identifiable Information (PII) or sensitive corporate data. Modern observability pipelines implement PII scrubbing *before* the trace leaves the application boundary.

## Lab and production

The [notebook](23_prompt_observability_and_failure_diagnosis.ipynb) demonstrates building a simulated `Tracer` class. It runs two scenarios (one successful, one failed). By inspecting the generated traces, you will identify that the failure wasn't caused by a bad prompt, but by stale data injected during the upstream `Retrieve Context` span. It also demonstrates how to implement a PII scrubber to redact sensitive information before logging the trace. Production systems use structured OpenTelemetry-compatible events, privacy controls, sampling, dashboards, alerts, incident playbooks, and linked release versions.

## References

- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
