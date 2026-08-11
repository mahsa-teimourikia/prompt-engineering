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

    classify decision → authorize sources → rank/select → label/structure
    → budget/compress → generate → validate and refresh

The [notebook](context_engineering.ipynb) compares a full packet with selected
evidence. The full packet includes an injection-like string; selection preserves
the relevant high-authority policy and lowers the token budget. The transparent
implementation is [lab.py](lab.py).

## Evaluation and production

Measure evidence recall, source authority, grounded answer quality, token use,
latency, and safe abstention separately. Test stale sources, conflicting
sources, lost-in-the-middle position, history summaries, memory poisoning, and
tool-output injection. Apply tenant and permission filtering before retrieval;
delimiters help interpretation but do not enforce security.

## References

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
