# Reasoning-oriented prompting: decomposition, verification, and search

## Use reasoning techniques for the right problem

Reasoning-oriented prompts are helpful when a task has intermediate dependencies: calculations, constraint satisfaction, evidence comparison, diagnosis, or planning. They are not a ritual phrase to append to every request. Modern reasoning-capable models may perform internal reasoning already; the useful engineering move is to specify the problem, evidence, constraints, verification criteria, and budget.

## Technique map

| Technique | Pattern | Best fit | Main cost/risk |
| --- | --- | --- | --- |
| Decomposition | split work into named stages | complex but known process | over-fragmentation |
| Chain-of-thought demonstrations | examples include intermediate reasoning | symbolic/multi-step tasks | extra tokens; do not expose private rationale as a requirement |
| Self-consistency | sample independent solutions then aggregate | answers with verifiable convergence | latency/cost multiplies |
| Tree-of-thought/search | generate, score, prune alternatives | planning or strategic choice | search explosion and weak self-scoring |
| Critique/revision | generate → review → revise | drafts with a concrete rubric | correlated errors |
| ReAct | reason, call tool, observe, update | external evidence is needed | tool misuse/looping |

## Step-by-step example: policy diagnosis

Northstar receives: “My refund was rejected. Explain why.” A weak prompt asks for an explanation. A stronger workflow says:

```text
1. Extract claimed facts from the customer message.
2. Retrieve the current approved eligibility policy and verified order facts.
3. List which eligibility conditions are satisfied, unsatisfied, or unknown.
4. Do not infer an unknown condition.
5. Draft an explanation only from verified evidence; otherwise ask a focused question.
```

This is decomposition, not necessarily an autonomous agent. Each stage has a small, testable output.

## Self-consistency with a budget

For a high-value but read-only analysis, generate several independent candidate classifications, validate each against policy, and aggregate only the allowed answer. Do not majority-vote unsupported claims. Use it when the expected improvement justifies N-times cost and latency; record agreement rate as a confidence signal, not as proof of truth.

```text
candidate answers → deterministic policy/evidence check → aggregate supported candidates
                              └→ all fail → escalate
```

## Tree search and critique

For a strategic recommendation, ask for materially different options, score them against explicit criteria, prune dominated options, and develop the strongest options. Use a separate critic call or a structured rubric for significant decisions. A critic should identify justified weaknesses—not redesign the solution for novelty.

## ReAct and verification

ReAct links a decision to external observation: `reason → permitted tool call → observation → updated decision`. The application owns tool execution, validates arguments, and caps steps. A model should not treat its own unverified intermediate text as evidence. Require a final claim-to-source mapping after tool use.

## Guided experiment

Compare a direct answer, a decomposed workflow, and a multi-sample approach on ten Northstar cases. Measure correctness, evidence support, number of calls, latency, and cost. Include an insufficient-evidence case: the best result is an escalation, not a confident consensus.

## References

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Self-Consistency](https://arxiv.org/abs/2203.11171)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [ReAct](https://arxiv.org/abs/2210.03629)
