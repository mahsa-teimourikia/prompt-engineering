# PromptOps: model-aware, tested, observable changes

PromptOps applies software delivery practices to prompts and context policies: versioned artifacts, test datasets, release gates, trace review, rollback, and monitoring. Portability does not mean identical wording works across models. Keep a stable behavioral contract and evaluate model-specific prompt variants against the same dataset.

Optimization should target the cheapest reliable system outcome, not the fewest prompt tokens. Automated optimizers can propose variants, but they must not overfit a small test set or bypass security and human review.

**References:** [DSPy](https://arxiv.org/abs/2310.03714), [OpenAI evals](https://platform.openai.com/docs/guides/evals), [Promptfoo](https://www.promptfoo.dev/docs/intro/).
