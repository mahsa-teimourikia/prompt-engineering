# 24 — Prompt Versioning, Experimentation, and Release Engineering

## Learning objectives

Version behavior manifests, gate candidates on evaluation, run shadow/canary
experiments, and roll back a release when observed error exceeds its threshold.

## Lab and production

The [notebook](prompt_versioning_experimentation_and_release_engineering.ipynb)
uses an evaluation gate and canary error rate to decide promotion.
[lab.py](lab.py) is an offline release policy. Production adds Git history,
registries, feature flags, audit logs, owner approval, telemetry, and a tested
rollback target. Never edit production behavior in place.

## References

- [Git documentation](https://git-scm.com/doc)
