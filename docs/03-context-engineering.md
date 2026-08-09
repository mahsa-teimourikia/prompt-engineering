# Context engineering: choose the evidence a model may use

Context engineering curates the information available at decision time: instructions, customer state, policy excerpts, prior turns, tools, and tool results. It is not “put everything in the context window.” More context can be stale, irrelevant, contradictory, or unsafe.

Design a context budget. Rank sources by authority and recency, attach provenance, separate trusted instructions from untrusted content, and summarize history without changing the source of truth. For grounded answers, explicitly require claim-to-evidence mapping and an abstention when evidence is insufficient.

**References:** [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Lost in the Middle](https://arxiv.org/abs/2307.03172).
