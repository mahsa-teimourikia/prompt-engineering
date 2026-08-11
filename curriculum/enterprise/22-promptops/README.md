# 22 — PromptOps

## Learning objectives

Package, version, test, release, observe, and roll back a complete behavior
artifact comprising prompt, model configuration, context policy, examples,
schemas, tools, permissions, evaluations, and runtime limits.

## Lab and production

The [notebook](promptops.ipynb) applies a release gate to an artifact.
[lab.py](lab.py) demonstrates required fields and an evaluation threshold.
Production PromptOps adds Git history, registries, CI, feature flags, canaries,
tracing, incident response, ownership, approvals, and rollback. Do not deploy
an edited prompt in place without its evaluated dependencies.

## References

- [OpenTelemetry](https://opentelemetry.io/docs/)
