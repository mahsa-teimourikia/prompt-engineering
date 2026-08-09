# Model-aware prompting: stable behavior across changing models

## Keep the contract constant; test the implementation

Models differ in instruction following, reasoning behavior, context capacity, tool use, multimodal capability, verbosity, safety behavior, and structured-output support. Do not assume a prompt migration is a string replacement.

Create a provider adapter that accepts the same task contract, schema, policy, and evaluation items. Allow model-specific prompt variants, but store them with the model/configuration version. Run regression evaluation before rollout and retain a rollback model/prompt pair.

| Question | Why it matters |
| --- | --- |
| Does the model support strict schema output? | Determines validation and repair behavior. |
| How are tools declared and tool results returned? | Changes orchestration state and error handling. |
| What is the context window and long-context behavior? | Changes selection/compression policy, not just token limit. |
| How are data retention and access handled? | Affects privacy and architecture. |
| Which evaluation slices regress? | Prevents a headline score from hiding failures. |

Use official provider documentation for current parameters and capabilities. Keep provider-specific recipes in this module; keep the rest of the course focused on durable system principles.

## References

- [OpenAI prompting](https://platform.openai.com/docs/guides/prompting)
- [Anthropic documentation](https://docs.anthropic.com/)
- [Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
