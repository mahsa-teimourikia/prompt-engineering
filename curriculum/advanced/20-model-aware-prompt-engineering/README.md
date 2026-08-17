# 20 — Model-Aware Prompt Engineering

## Learning Objectives
- **Build Portable Contracts:** Write prompts and schemas that are universally understood across foundational models.
- **Avoid Folklore:** Stop relying on model-specific hacks ("take a deep breath", specific XML tagging) unless proven by local evaluation.
- **Implement Unified SDKs:** Abstract provider-specific APIs behind a unified router interface.
- **Execute Data-Driven Selection:** Choose models based on automated evaluations of validity, cost, and latency on your specific schema.

## Core Concepts & Workflow

Prompt engineering has historically been plagued by "provider folklore"—superstitions like adding "take a deep breath" to every prompt because social media claimed it worked for GPT-4.

Modern AI engineering rejects folklore. Prompts and schemas should be portable across foundational models. Engineering is done at the contract layer (Pydantic schemas, explicit data modeling) rather than by hacking model-specific quirks. By using unified API abstractions, you can evaluate the exact same prompt against multiple models (e.g., Gemini Flash vs. Pro) to make data-driven decisions based on correctness, latency, and cost for *your specific use case*.

![Portable Prompt Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Believing "provider folklore" (e.g., adding "take a deep breath" to every prompt because Twitter said it works for GPT-4).

**Current State of the Art:** 
1. **Portable Contracts:** Prompts and schemas should be portable across foundational models. Engineering is done at the contract layer, not by hacking model-specific quirks.
2. **Unified SDK Abstractions:** Frameworks like **[LiteLLM](https://github.com/BerriAI/litellm)** or the new Google GenAI SDK provide unified interfaces so you can evaluate the exact same prompt against different models.
3. **Data-Driven Model Selection:** You choose between models (e.g., Flash vs. Pro) based on automated evaluation suites measuring correctness, latency, and cost on *your specific prompt contract*. General performance can be tracked on state-of-the-art leaderboards like the **[LMSYS Chatbot Arena](https://chat.lmsys.org/)**.

## Lab and Production

### The Lab
The [notebook](20_model_aware_prompt_engineering.ipynb) demonstrates evaluating the exact same Pydantic contract against two different models (`gemini-2.5-flash` and `gemini-2.5-pro`) using the unified Google GenAI SDK. It compares validity, cost (via token counting), and latency to demonstrate how to make data-driven decisions about model selection.

### Production Best Practices
- **Isolate Model Overrides:** If a specific model truly requires a unique quirk (e.g., a specific system prompt format), isolate that hack in a router layer, not in the core business logic.
- **Continuous Benchmarking:** Production comparisons should continuously evaluate instruction following, reasoning, structured output adherence, tool use capability, multimodality, safety, and version changes as models update.
- **Multi-Model Fallbacks:** Use unified SDKs to automatically fall back to an alternate provider if the primary model experiences an outage or severe latency spike.
