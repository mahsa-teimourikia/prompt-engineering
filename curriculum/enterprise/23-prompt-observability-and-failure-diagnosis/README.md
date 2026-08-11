# 23 — Prompt Observability and Failure Diagnosis

## Learning objectives

Trace behavior artifacts, model/configuration, context, examples, tools,
validation, evaluation, tokens, latency, and cost; then isolate deliberate
regressions without exposing sensitive content or private reasoning.

## Lab and production

The [notebook](prompt_observability_and_failure_diagnosis.ipynb) compares two
traces and identifies stale context as the responsible change. [lab.py](lab.py)
is an offline trace mechanism. Production systems use structured OpenTelemetry-
compatible events, privacy controls, sampling, dashboards, alerts, incident
playbooks, and linked release versions.

## References

- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
