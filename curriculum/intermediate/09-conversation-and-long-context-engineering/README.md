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

    history → classify current decision → window, summary, or retrieve
            → preserve source/state identifiers → answer or clarify

The [notebook](conversation_and_long_context_engineering.ipynb) compares four
strategies on the same history. [lab.py](lab.py) measures retained order and
preference facts plus a transparent context-size proxy.

## Evaluation and production

Measure retained task information, instruction retention, irrelevant context,
tokens, latency, and stale-summary errors. Test long histories, topic switches,
conflicting preferences, lost-in-the-middle positions, memory poisoning, and
privacy boundaries. Keep durable customer state separate from model summaries;
authorize and version every memory source.

## References

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Long-context guidance](https://ai.google.dev/gemini-api/docs/long-context)
