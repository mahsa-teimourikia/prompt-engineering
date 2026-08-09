# Prompt security and untrusted content

Prompt injection tries to make a system follow attacker-controlled instructions. It may arrive directly from a user or indirectly through a web page, document, tool response, or retrieved knowledge base. Delimit untrusted content, label it as data, and instruct the model never to follow instructions found inside it—but do not mistake that for a complete defense.

Defense in depth includes input/output controls, least-privilege tools, tenant filtering before retrieval, human approval for consequential actions, data minimization, monitoring, and incident response. A prompt must never grant permission.

**References:** [OWASP prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), [OpenAI safety best practices](https://platform.openai.com/docs/guides/safety-best-practices).
