# Prompt cost and latency engineering

## Optimize the reliable system outcome

Token count is a useful signal, not the objective. A good production metric is cost per successful, policy-compliant task. It includes model calls, retrieval/reranking, tool calls, retries, guardrails, and human review cost where relevant.

## Budget model

```text
task cost = input/output tokens + retrieval + tool calls + retries + guardrails
task latency = queue + model + retrieval + tool + approval/resume time
```

Measure median and tail latency, not only averages. A fast happy path can hide a retry or tool timeout that harms real users.

## Optimization sequence

1. Establish a quality and safety baseline.
2. Remove irrelevant context and duplicate tool calls.
3. Route simple tasks to a deterministic workflow or smaller capable model.
4. Cache stable, authorized results with correct tenancy and expiry.
5. Parallelize independent read operations only when it improves tail latency.
6. Re-evaluate quality, safety, cost, and latency after every change.

Never reduce evidence, validation, or approval just to improve a token metric. An inexpensive unsupported answer is not a success.

## Northstar example

A simple shipping-policy question should use one approved policy lookup and a schema validator. An investigation with order state and policy may use two read tools. A five-agent debate is unlikely to be economical unless comparison proves a material quality improvement. Record the trajectory so you can find duplicated searches, unnecessary reflections, and retry storms.

## References

- [OpenAI Evals](https://platform.openai.com/docs/guides/evals)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
