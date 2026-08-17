# 27 — Prompt Portability and Multi-Model Systems

## Learning Objectives
- **Avoid Vendor Lock-In:** Design systems that can easily swap foundational models (e.g., OpenAI to Google) without rewriting business logic.
- **Implement Unified SDKs:** Abstract provider-specific API idiosyncrasies behind unified routing layers.
- **Design Multi-Model Fallbacks:** Build resilient systems that automatically failover to a backup provider if the primary API experiences an outage.
- **Standardize Contracts:** Use programmatic schemas to ensure inputs and outputs remain consistent regardless of the underlying LLM.

## Core Concepts & Workflow

Tying an enterprise application directly to a specific provider's API (e.g., hardcoding OpenAI's exact JSON structure) is a massive strategic risk. It creates vendor lock-in, prevents you from utilizing better/cheaper models when they are released by competitors, and makes your application vulnerable to single-provider outages.

State-of-the-art architectures demand Prompt Portability. You must engineer your systems at the *Contract Layer*. By defining inputs and outputs via strict Pydantic schemas and using a unified proxy or SDK to translate those schemas into provider-specific API calls, you can hot-swap models instantly. If Provider A goes down, your code automatically routes the exact same Pydantic contract to Provider B.

![Portability Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Hardcoding `import openai` throughout the entire codebase and manually parsing specific response shapes.

**Current State of the Art:**
1. **Unified Proxies:** Tools like **[LiteLLM](https://github.com/BerriAI/litellm)** or **Portkey** act as universal translators. You write code using one standard API format, and the proxy translates it on the fly to Anthropic, Google, AWS Bedrock, or OpenAI.
2. **Provider-Agnostic SDKs:** Libraries like **LangChain** or the unified **Google GenAI SDK** abstract the underlying API mechanics, allowing you to switch the `model_name` string without changing any downstream parsing logic.
3. **Automated Fallbacks & Load Balancing:** Enterprise API gateways are configured to monitor the latency of Provider A. If it exceeds a 2-second threshold, the gateway automatically routes the prompt to Provider B, ensuring the end-user never experiences a timeout.

## Lab and Production

### The Lab
The [notebook](27_prompt_portability_and_multi_model_systems.ipynb) demonstrates true portability. It defines a complex extraction task and a rigid Pydantic schema, and then executes that exact same code block against two completely different model families (e.g., Gemini and a local open-weights model). It proves that the application code does not need to change when the model changes.

### Production Best Practices
- **Test Fallbacks Continuously:** A fallback model is useless if you haven't tested it. Run your automated evaluation suite against your fallback models weekly to ensure they still meet your minimum quality thresholds.
- **Normalize Telemetry:** Different providers report token usage differently. Your unified proxy must normalize these metrics so your cost dashboards remain accurate regardless of which model served the request.
- **Beware Capability Gaps:** Portability of *code* does not mean portability of *capability*. Just because a smaller open-source model accepts the same JSON schema doesn't mean it has the reasoning power to successfully fill it out.
