# Prompt technique catalog: choose a pattern by problem, not fashion

## How to use this catalog

Start with a task contract and evaluation set. Then select the simplest technique that addresses an observed failure. A technique is not automatically an improvement: it can add cost, latency, fragility, or a new security boundary.

| Technique | What it changes | Use when | Avoid when |
| --- | --- | --- | --- |
| Zero-shot | Clear task/constraints only | familiar task, intuitive labels, simple output | the boundary or format is repeatedly misunderstood |
| One-/few-shot | Demonstrated input/output boundary | labels, format, style, edge cases need clarification | examples are stale, confidential, or near-duplicate |
| Role framing | Decision perspective | a review rubric or audience matters | it is only flattering persona text |
| Decomposition | Named intermediate operations | work has known stages | a direct deterministic function would suffice |
| Prompt chaining | Output of one step feeds next | each stage benefits from validation | hidden chain state cannot be observed |
| Generated knowledge | model drafts facts before task | hypotheses can be independently checked | generated “facts” will be treated as evidence |
| Query rewriting/multi-query | alternate retrieval formulations | recall is the bottleneck | query expansion leaks tenant data or overwhelms retrieval |
| Chain-of-thought examples | intermediate reasoning demonstrations | multi-step symbolic tasks | privacy requires hidden rationale or model reasons internally |
| Self-consistency | multiple samples/aggregation | high-value, verifiable answer with ambiguity | majority agreement is mistaken for evidence |
| Tree/search | create-score-prune alternatives | planning/strategy with explicit criteria | scoring is unreliable or exploration cost is unjustified |
| Critique/revision | draft against rubric then revise | quality can be checked by clear rubric | same model's critique is accepted unverified |
| ReAct | choose tool, observe, update | external evidence/action changes the path | a fixed workflow is adequate |
| PAL/program-aided | delegate calculation to deterministic code | arithmetic, tables, logic can be executed safely | arbitrary code execution is exposed |
| Active prompting | focus labels/review on uncertain examples | building an evaluation/training set | uncertainty sampling excludes safety-critical cases |
| Directional stimulus | provide hints/key phrases | controlled generation or retrieval alignment | hints are treated as factual evidence |
| Graph prompting | represent relationships explicitly | multi-hop entities/relationships matter | graph construction is more complex than the task |

## Mini patterns

### Zero-shot versus few-shot

```text
Task: classify the support request as refund, shipping, account, or unknown.
Return only the label.
```

Add few-shot demonstrations only after an eval shows a boundary failure. A useful contrast example is: “Where is my order?” → `shipping`; “What is the return window?” → `refund`; “Please reset my password” → `account`.

### Generate → critique → revise

```text
Draft: create a response using approved evidence only.
Critique: find unsupported claims, missing required fields, and policy conflicts.
Revision: repair only confirmed issues; preserve citations.
```

The critique must have the same evidence and a rubric. For consequential use, validate final claims in code or human review.

### Query transformation

```text
User: “Why was my claim rejected?”
Retrieval queries: “claim rejection eligibility criteria”; “required documentation”; “policy exclusions”.
```

Merge and rerank results, preserve their sources, and still apply tenant/freshness filters before the model sees them.

## Technique selection worksheet

For a candidate technique, record: failure observed; baseline score; proposed mechanism; extra calls/tokens; security impact; expected metric; stop/rollback criterion. If you cannot state the expected metric, do not add the technique yet.

## References

- [The Prompt Report](https://arxiv.org/abs/2406.06608)
- [A systematic survey of prompt engineering](https://arxiv.org/abs/2402.07927)
- [Chain-of-Thought](https://arxiv.org/abs/2201.11903), [Self-Consistency](https://arxiv.org/abs/2203.11171), [Tree of Thoughts](https://arxiv.org/abs/2305.10601), [ReAct](https://arxiv.org/abs/2210.03629)
