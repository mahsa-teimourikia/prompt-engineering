# 08 — Context Engineering

## Learning Objectives
- **Understand Context Limits:** Learn the mechanics of token windows and how models process injected data.
- **Structure Injected Data:** Use XML tags or Markdown to cleanly demarcate background context from active instructions.
- **Prevent Lost in the Middle:** Mitigate the phenomenon where models ignore data placed in the center of massive context blocks.
- **Implement Pruning Strategies:** Design programmatic rules for safely truncating data when context limits are reached.

## Core Concepts & Workflow

Language models do not have access to your private databases or the internet by default. To make them useful for enterprise tasks, you must inject relevant background information directly into the prompt. This is Context Engineering.

However, context is not infinite, and it is not free. Even with modern massive context windows, injecting poorly structured data leads to confusion. If you dump a raw CSV file and a raw JSON log into the prompt without clear delimiters, the model will struggle to differentiate the instructions from the data. Furthermore, models suffer from the "Lost in the Middle" phenomenon—they pay high attention to the very beginning and very end of a prompt, but often ignore data buried in the middle.

![Context Engineering Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Copy-pasting raw text into the user input field alongside the question.

**Current State of the Art:**
1. **Explicit Delimiters:** Industry standard prompts use strict XML-style tags (e.g., `<background_documents> ... </background_documents>`) to encapsulate context. Models are heavily fine-tuned to recognize these structural boundaries.
2. **Massive Context Models:** Models like Gemini 1.5 Pro natively support 2 million+ tokens. This allows entire codebases or libraries to be injected as context, shifting the engineering challenge from "fitting data in" to "structuring data clearly."
3. **Context Caching:** To mitigate the extreme cost and latency of injecting millions of tokens per request, providers now offer **Context Caching APIs**. You upload the massive context once, and subsequent queries execute against the cached memory almost instantly.

## Lab and Production

### The Lab
The [notebook](08_context_engineering.ipynb) demonstrates how to cleanly structure a prompt using XML delimiters. It shows a failure case where a model hallucinates because the context is messy, and fixes it by cleanly separating the `<instructions>` from the `<support_history>` and `<current_ticket>`.

### Production Best Practices
- **Data Hierarchy:** Always place the most critical information (the final instructions and the most relevant facts) at the very end of the prompt, closest to where the model begins generating tokens.
- **Token Tracking:** You must programmatically calculate the token size of your context *before* making the API call. If it exceeds your budget or the model limit, you must execute a fallback pruning strategy.
- **Sanitize Context:** Never inject raw HTML or massive unformatted system logs if you only need the text. Pre-process and strip noise from your data to save tokens and improve model focus.
