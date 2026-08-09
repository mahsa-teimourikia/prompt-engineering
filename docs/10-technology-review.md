# Technology review

| Need | Useful technologies | Decision guidance |
| --- | --- | --- |
| Model-specific prompting | OpenAI, Anthropic, Gemini official SDKs | Follow the target model's current guidance; keep provider calls behind an adapter. |
| Typed output | JSON Schema, Pydantic, provider structured output | Validate at the application boundary, even after constrained decoding. |
| Prompt/program optimization | DSPy, promptfoo | Establish a representative eval set before optimization. |
| Evaluation and tracing | OpenAI Evals, LangSmith, Phoenix, promptfoo | Combine deterministic checks, rubric judging, and sampled human review. |
| Tool/agent orchestration | OpenAI Agents SDK, LangGraph, semantic-kernel | Use only when state, tools, or routing justify the added complexity. |
| Prompt security | OWASP guidance, guardrail layers, policy engines | Authorization and data isolation must live outside the prompt. |

Open source and vendor tools change quickly. Evaluate their security posture, data-handling terms, observability, and ability to export prompt/eval artifacts before adoption.
