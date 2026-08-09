# RAG and tool-use prompt interfaces

RAG supplies external evidence; tools query or act on systems. Their interfaces are prompts too: clear tool names, narrow descriptions, typed arguments, and predictable errors help a model choose safely. Require evidence before a policy claim; let the model ask a clarification when a lookup needs a missing identifier.

Never turn tool output into trusted instruction. Treat it as untrusted data, validate arguments in code, and enforce permissions outside the model. Use bounded retries and distinguish retryable timeout failures from permission failures that require escalation.

**References:** [ReAct](https://arxiv.org/abs/2210.03629), [Toolformer](https://arxiv.org/abs/2302.04761), [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling).
