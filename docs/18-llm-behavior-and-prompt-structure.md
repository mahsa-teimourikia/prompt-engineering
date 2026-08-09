# How LLM prompting works: model behavior, sampling, and structure

## Why this matters

Two people can send the same well-written prompt and receive different outputs across models, configurations, or runs. Before adding techniques, learners need a working model of the inference environment: instructions, context window, available tools, conversation state, sampling configuration, and model capability together determine the output.

## The inference model

```text
model + instruction hierarchy + selected context + examples + tools/state
       + sampling configuration → candidate output → validation/action
```

Prompt engineering changes information and constraints at inference time; it does not change model weights. It is iterative engineering: define a target behavior, observe failure, make a measured change, and evaluate the result.

## Instruction hierarchy and boundaries

System/application rules establish durable behavior; user requests express a task; retrieved documents and tool results are data. Use headings or XML-style tags consistently so a model can parse the structure, but enforce authorization, tenancy, and side-effect controls in code.

```text
<objective>Draft a policy-grounded support response.</objective>
<constraints>Use approved evidence only. Do not execute actions.</constraints>
<context>…evidence and user data…</context>
<response_format>CaseBrief JSON</response_format>
```

## Sampling controls: trade-offs, not quality sliders

| Control | Typical effect | Practical use |
| --- | --- | --- |
| Temperature | higher values broaden variation; lower values reduce variation | use lower variance for classification/extraction; test higher variance for ideation or self-consistency. |
| Top-p | restricts candidate-token probability mass | change deliberately; do not tune temperature and top-p blindly together. |
| Max output tokens | bounds response length/cost | set enough room for required schema; detect truncation. |
| Reasoning budget, where supported | trades extra deliberation for cost/latency | reserve for problems whose eval shows a quality gain. |
| Seed/deterministic modes, where supported | helps reproduce tests but does not guarantee semantic stability | use for debugging; keep robustness tests. |

## Prompt structure patterns

Use a consistent template: role/decision frame, objective, trusted context, constraints, examples, output contract, and failure path. Markdown works well for readable sections; XML-like tags make machine-assembled components visually explicit. The important property is consistency and clear instruction/data separation, not a specific markup style.

## Guided experiment

For one Northstar classification case, run a baseline across several sampling settings. Record label agreement, schema validity, latency, and cost. Then repeat on an ambiguous case. The goal is not to find a universally “best” temperature; it is to choose a configuration justified by the task and evaluation set.

## When not to tune prompts

Do not use wording or sampling to compensate for missing access control, absent source data, invalid tool arguments, or an undefined business decision. First repair the system boundary or data source.

## References

- [Google prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting)
- [The Prompt Report](https://arxiv.org/abs/2406.06608)
