# Instruction contracts: establish the task before optimizing wording

A useful prompt specifies an objective, the available facts, operating constraints, output format, and success conditions. This prevents a common failure: a fluent answer that silently invents policy or answers the wrong user need.

For Northstar, compare `Answer this customer` with a contract: *Classify the request. Use only supplied policy excerpts. State uncertainty. Return the defined case schema. Do not promise refunds or actions.* The latter is inspectable and testable.

Use direct, consistent instructions and delimit data from instructions. Do not rely on role language as access control; it only helps the model understand a job. Keep authorization, rate limits, and side effects in code.

**Failure modes:** ambiguous verbs, incompatible constraints, hidden success criteria, and including untrusted text without marking it as data.

**References:** [Google guidance](https://ai.google.dev/gemini-api/docs/prompting-strategies), [Prompt Report](https://arxiv.org/abs/2406.06608).
