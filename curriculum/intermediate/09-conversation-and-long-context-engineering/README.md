# 09 — Conversation and Long-Context Engineering

## Learning objectives

Choose a conversation-state strategy, measure retained task facts and context
cost, and handle topic changes, stale instructions, summaries, and retrieval
without assuming a larger context window solves the problem.

## Scenario

A customer-success assistant must remember that order 42 is delayed and that
the user prefers email updates after unrelated discussion. Full history is
expensive; a sliding window can lose facts; summaries can become stale; and
history retrieval can miss relevant state.

## Mental model and lab

![Mental Model Diagram](./diagram-1.svg)

The [notebook](09_conversation_and_long_context_engineering.ipynb) compares three
strategies on the same history: a Sliding Window (which forgets old facts), a Summary 
Memory (which can suffer from decay), and Structured State Extraction (which continuously
extracts and persists critical entities like Order IDs using Pydantic).

## Technology landscape and state of the art

**Foundational:** Understanding that passing the entire chat history in every prompt is inefficient, expensive, and leads to models forgetting instructions (the "Lost in the Middle" phenomenon).

**Current State of the Art:**
1. **Massive Context Caching:** With models supporting up to 2 million tokens, some teams opt to cache the entire user history. This is powerful but doesn't solve cross-session memory (e.g., remembering a user's preference from a chat they had 3 months ago on a different device).
2. **Structured State Checkpointing:** The gold standard for production conversational AI (used by frameworks like LangGraph) is keeping a rigid "State Object" (e.g., a Pydantic model containing `order_id`, `user_intent`, `sentiment`). After every message, the LLM updates this state object. The prompt then includes a small sliding window of recent messages PLUS the current State Object, ensuring critical facts are never lost.

## Evaluation and production

Measure retained task information, instruction retention, irrelevant context, tokens, latency, and stale-summary errors. Test long histories, topic switches, conflicting preferences, lost-in-the-middle positions, memory poisoning, and privacy boundaries. Keep durable customer state separate from model summaries; authorize and version every memory source.

## References

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Long-context guidance](https://ai.google.dev/gemini-api/docs/long-context)
