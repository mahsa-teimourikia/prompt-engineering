# Examples, constraints, and structured output

Examples demonstrate a task boundary; they are not a substitute for requirements. Choose varied examples that include edge cases, keep their labels consistent, and evaluate whether they improve the held-out set. A schema makes the expected interface explicit: software validates fields, types, allowed values, and missing evidence before an answer reaches a customer.

In production, use provider-native structured output when available, then validate again in your application. Retrying an invalid response needs a bounded repair policy and must preserve the original inputs for audit.

**References:** [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs), [Pydantic](https://docs.pydantic.dev/), [in-context learning survey](https://arxiv.org/abs/2406.06608).
