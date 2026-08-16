# 08 — Context Engineering

## Learning objectives

Select, prioritize, structure, compress, isolate, and refresh the context
packet; compare full context with selected authorized evidence; and measure
quality, token use, latency, and unsafe-context exposure.

## Why this matters

The effective request includes instructions, user input, history, examples,
retrieval, memory, tools, tool results, and application state. More context is
not better context. Northstar’s policy assistant must preserve an approved
policy while excluding malicious or stale text.

## Mental model and lab

![Mental Model Diagram](./diagram-1.svg)

The [notebook](08_context_engineering.ipynb) compares a naive "data dump" approach
against proper context engineering. The data dump includes a hidden prompt injection
within a user's history, causing the model to break policy. The engineered context
demonstrates filtering out irrelevant data and using strict XML tagging to isolate
the untrusted user input from the system policy.

## Technology landscape and state of the art

**Foundational:** Delimiting system instructions from untrusted user input to prevent context poisoning.

**Current State of the Art:**
1. **Massive Context Windows:** Models like Gemini 1.5 Pro now support up to 2 million tokens. This fundamentally shifts the landscape from "How do I compress this?" to "How do I effectively organize this massive ocean of data so the model doesn't get confused?"
2. **Context Caching:** With massive context comes massive cost and latency. Context Caching allows you to load an entire repository or corpus of documents into the model's memory once, and then query it repeatedly at a fraction of the cost and latency.
3. **Retrieval-Augmented Generation (RAG):** For datasets larger than 2M tokens (or datasets that update constantly), RAG remains the standard. The focus has shifted from simple semantic search to complex GraphRAG and hybrid search techniques to improve the quality of the retrieved context.

## Evaluation and production

Measure evidence recall, source authority, grounded answer quality, token use, latency, and safe abstention separately. Test stale sources, conflicting sources, lost-in-the-middle position, history summaries, memory poisoning, and tool-output injection. Apply tenant and permission filtering before retrieval; XML delimiters help interpretation and boundary setting.

## References

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
