# 27 — Prompt Portability and Multi-Model Systems

## Learning objectives

Separate portable contracts from provider adaptations, detect features, compare
fallbacks, and run a migration suite before changing models.

## Lab and production

The [notebook](prompt_portability_and_multi_model_systems.ipynb) compares an old
and new adapter and detects a quality regression despite schema compatibility.
[lab.py](lab.py) demonstrates the migration boundary. Production systems version
adapters, maintain per-model regression suites, test structured output/tool/
context differences, and isolate necessary overrides.

## References

- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting)
