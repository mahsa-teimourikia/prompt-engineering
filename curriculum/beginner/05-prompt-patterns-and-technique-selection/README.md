# 05 — Prompt Patterns and Technique Selection

**Level:** Beginner · **Estimated time:** 60–90 min · **Prerequisites:** Courses 01–04 and basic regular expressions

## Learning Objectives

- **Map Failures to Techniques:** Learn to identify a specific observed failure and select the *smallest* prompt technique required to address it.
- **Avoid Pattern Bloat:** Understand the hidden costs (latency, tokens, unreliability) of applying every known prompt technique simultaneously.
- **Measure Justification:** Define the exact metric that justifies the added architectural complexity of a new technique.
- **Establish a Selection Hierarchy:** Master the progression from Direct Instructions -> Schemas -> Few-Shot -> Retrieval -> Agents.

## Scenario

Northstar extracts product codes from support messages. Codes normally match
`PRD-####`, but a message may also contain order numbers, prose, or a
lowercase/space variant. The lab starts with the smallest possible technique,
measures failures, adds a system instruction, adds one boundary example, and
then compares the result with deterministic code.

## Core Concepts & Workflow

A technique catalog is useful reference material, not an architecture. Adding deep personas, massive few-shot examples, chain-of-thought reflection, RAG retrieval, and agentic tool-use to every single task creates massive token costs and completely obscures the root causes of failures.

Engineering is about minimizing complexity. You must start with the simplest possible approach (a measurable Instruction Contract). Only when that contract fails—and you can prove it fails against a frozen evaluation suite—do you introduce the next level of complexity to address that specific failure mode.

![Mental Model Diagram](./diagram-1.svg)

## Deep dive

### 1. Context and evidence patterns

| Technique | Mechanism | Use when | Do not use when | Learn it here |
| --- | --- | --- | --- | --- |
| **Context selection** | Choose the smallest authorized set of instructions, state, and evidence. | A response needs current task-specific information. | “More context” is being used as a substitute for source quality. | [Context engineering](../../intermediate/08-context-engineering/README.md) · [Notebook 03](../../../curriculum/intermediate/08-context-engineering/08_context_engineering.ipynb) |
| **Context compression** | Summarize, extract, or retain only decision-relevant state with provenance. | Long history crowds out current evidence. | A summary discards the legal, numerical, or contradictory detail needed later. | [Context engineering](../../intermediate/08-context-engineering/README.md) |
| **Retrieval-augmented generation (RAG)** | Retrieve approved sources and answer from their evidence. | Knowledge changes, is too large for the prompt, or requires citations. | The answer is actually a live transactional fact better obtained from a tool. | [RAG and tools](../../../docs/04-rag-tools.md) · [Notebook 04](../../../curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/10_evidence_grounded_prompting_and_rag_interfaces.ipynb) |
| **Query rewriting / multi-query retrieval** | Create alternate search formulations, merge, then rerank results. | Retrieval recall—not generation quality—is the measured bottleneck. | Expanded queries can cross tenant boundaries, amplify noise, or exceed latency budget. | [RAG and tools](../../../docs/04-rag-tools.md) · [Application playbooks](../../../docs/15-application-playbooks.md) |
| **HyDE / hypothetical-document retrieval** | Draft a hypothetical answer/document to use as a retrieval query. | Semantic retrieval misses terminology or sparse queries. | The hypothetical text is shown as evidence or substitutes for source retrieval. | [RAG and tools](../../../docs/04-rag-tools.md) |
| **Cited generation / quote-then-answer** | Require source IDs or evidence excerpts for material claims. | Users need auditability and the system may need to abstain. | Citation presence is accepted without checking that the source entails the claim. | [Context engineering](../../intermediate/08-context-engineering/README.md) · [Evaluation](../../advanced/14-prompt-evaluation/README.md) |
| **Memory retrieval** | Retrieve validated, scoped user or task facts from durable storage. | Repeated interactions need stable preferences or case state. | Stale or unreviewed memory can bias a new decision. | [Context engineering](../../intermediate/08-context-engineering/README.md) · [Agentic prompts](../../../docs/08-agentic-prompts.md) |

**Safety note:** retrieved documents, search results, tool output, and user text are data—not instructions. Authorization filters must run before retrieval, and model instructions must never grant access to sources or tools. See [Prompt security](../../intermediate/13-prompt-security-and-untrusted-content/README.md).

### 2. Reasoning, planning, and verification patterns

| Technique | Mechanism | Use when | Do not use when | Learn it here |
| --- | --- | --- | --- | --- |
| **Task decomposition** | Break a known task into named, inspectable stages. | Different stages need different checks or inputs. | A deterministic function or direct answer already solves it. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) |
| **Chain-of-thought (CoT) examples** | Demonstrate intermediate reasoning for a multi-step task. | Small, well-defined symbolic or analytical tasks benefit from worked examples. | Internal rationale is needed for audit; request concise evidence or verifiable artifacts instead. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) · [CoT paper](https://arxiv.org/abs/2201.11903) |
| **Least-to-most / plan-and-solve** | Solve prerequisite subproblems before the final task. | A task has a dependency order that is known and checkable. | The plan is treated as proof or the task needs external evidence. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) · [Least-to-most](https://arxiv.org/abs/2205.10625) · [Plan-and-Solve](https://arxiv.org/abs/2305.04091) |
| **Self-consistency** | Sample multiple independent solutions and aggregate. | Answers are independently verifiable and ambiguity is real. | A majority vote is mistaken for evidence or cost is unjustified. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) · [Self-Consistency](https://arxiv.org/abs/2203.11171) |
| **Critique → revise / reflection** | Inspect a draft with a rubric, then repair confirmed defects. | Quality rules are explicit and the critique has access to the same evidence. | The same model's unverified critique is accepted as a guarantee. | [Evaluation](../../advanced/14-prompt-evaluation/README.md) · [Reliability](../../../docs/19-reliability-and-human-centred-ai.md) · [Reflexion](https://arxiv.org/abs/2303.11366) |
| **Tree of Thoughts (ToT)** | Generate, score, and prune several candidate reasoning paths. | Search choices are meaningful and a reliable scorer or verifier exists. | The scoring signal is vague, or exploration cost outweighs benefit. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) · [ToT paper](https://arxiv.org/abs/2305.10601) |
| **Graph of Thoughts** | Merge and transform dependent partial results as a graph. | Complex work has reuse or dependency across branches. | A simple chain is sufficient or graph bookkeeping is opaque. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) · [Graph of Thoughts](https://arxiv.org/abs/2308.09687) |
| **Generated knowledge** | Draft a hypothesis or background statement before solving a task. | The hypothesis can be independently checked against tools or sources. | Generated text will be treated as trusted evidence. | [Context engineering](../../intermediate/08-context-engineering/README.md) · [Reliability](../../../docs/19-reliability-and-human-centred-ai.md) |

#### Decision rule: search needs a verifier

Tree, graph, and multi-sample techniques create alternatives. They are only as sound as their scorer. If you cannot explain how a candidate is verified—by a test, calculation, source, rubric, or reviewer—prefer a simpler direct workflow.

### 3. Tool, program, and agent patterns

| Technique | Mechanism | Use when | Do not use when | Learn it here |
| --- | --- | --- | --- | --- |
| **Function / tool calling** | Ask the model to select a bounded operation with typed arguments. | Current facts or deterministic actions are needed. | A free-form “admin API(command)” exposes broad authority. | [RAG and tools](../../../docs/04-rag-tools.md) · [Agentic prompts](../../../docs/08-agentic-prompts.md) |
| **ReAct** | Alternate decision, tool action, observation, and updated decision. | Evidence changes the next step and the path cannot be known upfront. | A fixed workflow has known steps and fewer failure modes. | [Agentic prompts](../../../docs/08-agentic-prompts.md) · [ReAct paper](https://arxiv.org/abs/2210.03629) |
| **Program-aided language models (PAL) / program of thought** | Translate a problem into constrained executable logic; use a runtime for calculation. | Arithmetic, tables, transformations, or formal checks are safer in code. | Arbitrary generated code is executed with credentials or unrestricted access. | [Reasoning techniques](../../../docs/11-reasoning-techniques.md) · [PAL paper](https://arxiv.org/abs/2211.10435) |
| **Tool-use learning / Toolformer-style patterns** | Teach or optimize when an external tool is useful. | A model must choose among well-described, narrow tools. | Tool permissions and arguments are delegated to prompt text alone. | [RAG and tools](../../../docs/04-rag-tools.md) · [Toolformer](https://arxiv.org/abs/2302.04761) |
| **Prompt chaining** | Feed a bounded, inspectable artifact from one step to the next. | Each stage has a different contract and can be validated. | Hidden chain state makes failures impossible to inspect or replay. | [Application playbooks](../../../docs/15-application-playbooks.md) · [PromptOps](../../enterprise/22-promptops/README.md) |
| **Router → specialist** | Classify a request, then invoke a narrow workflow or specialist. | Task families are separable and routes can be evaluated. | The route has low confidence and no escalation path. | [Application playbooks](../../../docs/15-application-playbooks.md) · [Agentic prompts](../../../docs/08-agentic-prompts.md) |
| **Evaluator–optimizer loop** | Generate a candidate, evaluate against a rubric/tests, make bounded revisions. | An objective, testable score exists. | The evaluator is subjective, biased, or has no access to evidence. | [Evaluation](../../advanced/14-prompt-evaluation/README.md) · [PromptOps](../../enterprise/22-promptops/README.md) |

Tool schemas, permission checks, rate limits, idempotency, budgets, retries, and human approvals are **application controls**. A strong prompt can request them; it cannot enforce them. Continue with [Context Engineering](../../intermediate/08-context-engineering/README.md), [Prompt Security](../../intermediate/13-prompt-security-and-untrusted-content/README.md), [Prompt Evaluation](../../advanced/14-prompt-evaluation/README.md), and [PromptOps](../../enterprise/22-promptops/README.md).

### 4. Optimization and adaptation patterns

| Technique | Mechanism | Use when | Do not use when | Learn it here |
| --- | --- | --- | --- | --- |
| **Prompt versioning and A/B comparison** | Treat prompts, templates, context policy, and model settings as release artifacts. | A change must be attributable and reversible. | A “better” prompt is promoted from anecdotes. | [PromptOps](../../enterprise/22-promptops/README.md) · [Evaluation](../../advanced/14-prompt-evaluation/README.md) |
| **Automatic prompt optimization** | Search or synthesize prompt candidates against a held-out evaluation set. | The task has stable metrics and human-reviewed constraints. | The optimizer is trained and judged on the same small set, or safety cases are absent. | [Evaluation-driven prompt optimization](../../../docs/21-evaluation-driven-prompt-optimization.md) |
| **Active prompting** | Prioritize uncertain or informative examples for labeling/review. | Building a dataset with limited reviewer time. | Uncertainty sampling excludes rare safety-critical failures. | [Evaluation](../../advanced/14-prompt-evaluation/README.md) · [Prompt optimization](../../../docs/21-evaluation-driven-prompt-optimization.md) |
| **Model-aware adaptation** | Adjust prompt shape, capabilities, and fallbacks by model/version. | A system supports multiple models or is migrating versions. | It becomes model-locked without a durable behavioral contract. | [Model-aware guidance](../../../docs/16-model-aware-guidance.md) |
| **Caching and prompt compression** | Reuse stable prefixes and reduce redundant context. | Cost or latency is measured as a production bottleneck. | Compression removes evidence or caching risks privacy/correctness. | [Cost and latency](../../../docs/13-cost-latency-engineering.md) |
| **Fine-tuning instead of prompting** | Change learned behavior with curated training data. | Evaluation shows a stable, repeated task remains unreliable or too expensive with prompting alone. | A prompt/data problem is being hidden behind a training job. | [Technology review](../../../docs/10-technology-review.md) · [Model-aware guidance](../../../docs/16-model-aware-guidance.md) |

### 5. Safety, reliability, and human-centred patterns

| Technique or control | Mechanism | Use when | Learn it here |
| --- | --- | --- | --- |
| **Abstention / clarification** | Return an explicit unknown state or ask for missing evidence. | The answer is not supported or confidence/risk policy says not to automate. | [Reliability](../../../docs/19-reliability-and-human-centred-ai.md) · [Application playbooks](../../../docs/15-application-playbooks.md) |
| **Evidence-first answer** | Separate source-backed claims from hypotheses and recommendations. | A decision depends on current, auditable information. | [Context engineering](../../intermediate/08-context-engineering/README.md) · [RAG and tools](../../../docs/04-rag-tools.md) |
| **Input trust boundary** | Label user, retrieved, tool, and system content by trust level. | Any external content reaches the model. | [Prompt security](../../intermediate/13-prompt-security-and-untrusted-content/README.md) |
| **Output validation** | Parse/validate outputs before using them in software or tools. | Outputs drive routes, databases, or actions. | [Structured outputs](../../../curriculum/beginner/04-structured-outputs-and-typed-interfaces/README.md) · [Prompt security](../../intermediate/13-prompt-security-and-untrusted-content/README.md) |
| **Human approval gate** | Pause before high-impact actions and record approve/modify/reject. | Money, data, production systems, safety, or legal decisions are involved. | [Reliability](../../../docs/19-reliability-and-human-centred-ai.md) · [Agentic prompts](../../../docs/08-agentic-prompts.md) |
| **Adversarial / regression evaluation** | Test prompt injection, ambiguity, privacy, drift, and previous failures. | Before release and after every material prompt/model/tool change. | [Evaluation](../../advanced/14-prompt-evaluation/README.md) · [PromptOps](../../enterprise/22-promptops/README.md) |

### What this catalog intentionally does not claim

No catalog is a universal ranking. Results vary by model, task, domain, prompt budget, dataset, and evaluation design. Many named techniques overlap: a “planner,” “chain,” or “reflection” system may be the same underlying pattern with a different control loop. Prefer clear contracts, traceable evidence, and measured outcomes over fashionable labels.

Continue with [Context Engineering](../../intermediate/08-context-engineering/README.md), [Prompt Security](../../intermediate/13-prompt-security-and-untrusted-content/README.md), [Prompt Evaluation](../../advanced/14-prompt-evaluation/README.md), and [PromptOps](../../enterprise/22-promptops/README.md).

## Technology Landscape and State of the Art

**Foundational:** Blindly applying every technique from a blog post (e.g., "always use Chain of Thought") without measuring its impact.

**Current State of the Art:**
1. **Automated Optimization:** The field is moving away from manual "prompt hacking" toward automated compilation. Frameworks like **[DSPy](https://github.com/stanfordnlp/dspy)** treat the prompt as a program, using optimizers to automatically select the best combination of instructions and few-shot examples to maximize a defined metric.
2. **Evaluation-Driven Development:** Teams now spend more time building robust evaluation datasets (using tools like **LangSmith** or **Braintrust**) than writing prompts. A technique is only accepted if the CI/CD pipeline shows a statistically significant improvement on the eval set without regressions.
3. **Compound AI Systems:** Moving from single large prompts to graphs of smaller, specialized calls (e.g., using **[LangGraph](https://langchain-ai.github.io/langgraph/)**). Each node in the graph uses only the minimal techniques required for its specific, narrow sub-task.

## Lab walkthrough

- Phase 1 zero-shot records 1/3 on the original suite.
- Phase 2 system instruction records 2/3; `multiple_numbers` returns `88412`
  and remains wrong.
- Phase 3 few-shot records 3/3 on the original suite and succeeds on the
  recorded `formatted_variant`.
- Phase 4 uses `validate_code(text)` with exact regex matching. Regex scores
  3/3 on the original suite at zero tokens but fails on lowercase `prd 9921`.
- The worksheet renders a small technique catalog dictionary as Markdown.

### Implementation detail

The [notebook](05_prompt_patterns_and_technique_selection.ipynb) demonstrates the empirical process of technique selection. It establishes a Zero-Shot baseline, measures a specific failure mode (conversational filler), applies a System Instruction to fix it, and then measures the delta. It then observes a second boundary failure and introduces a targeted Few-Shot example to address it, proving the value of incremental technique application.

## Exercises

1. Add a new exact-format case to `fixtures/cases.json` and watch the phase
   accuracy numerator over its denominator.
2. Change the regex in `validate_code` and watch the zero-token metric on the
   original suite.
3. Add a boundary example to `_prompt` and watch few-shot accuracy on
   `multiple_numbers` and `formatted_variant`.

### Reflection questions

## Checkpoint

1. What was the measured Phase 1 result? **1/3 on the original suite.**
2. Which case remains wrong after the system instruction? **`multiple_numbers`,
   where the recorded output is `88412`.**
3. What is the lesson’s conclusion? **Measure, then pick the simplest tool that
   meets the requirement.**

## Production Best Practices

- **Complexity is a Liability:** Always default to the simplest architecture. (Code > Prompt > Schema > Few-Shot > RAG > Tools > Agents).
- **Rollback Together:** Version the problem statement, the technique choice, the evaluation cases, and the prompt together. If a technique is rolled back, the evaluation expectations must roll back with it.
- **Track Latency Costs:** Every technique (especially Chain-of-Thought or Agents) adds significant latency. Ensure the quality gain justifies the SLA hit.

## Further reading

The catalog is a decision aid, not a recipe to apply everywhere. Start with a
direct instruction and contract. Add contrastive examples for a label or
format boundary, a schema for an unreliable interface, retrieval for missing
knowledge, tools for live bounded data, and a planner/verifier workflow only
for genuinely complex subproblems. Ask what the smallest intervention is,
which frozen evaluation case proves it helped, and what regression it might
introduce. Track quality, latency, token use, operational complexity, and
rollback cost. Deterministic code is often preferable for exact extraction,
normalization, routing, and arithmetic; a prompt is useful when language
understanding or flexible interpretation is the hard part. Compound systems
should keep each node narrow and measurable rather than hiding every concern
inside one giant prompt.

References: [DSPy](https://github.com/stanfordnlp/dspy),
[LangGraph](https://langchain-ai.github.io/langgraph/),
[LangSmith](https://www.langchain.com/langsmith), and
[Braintrust](https://www.braintrust.dev/).

### Legacy references

- [The Prompt Report: A Systematic Survey of Prompting Techniques](https://arxiv.org/abs/2406.06608) — broad taxonomy and terminology.
- [A systematic survey of prompt engineering](https://arxiv.org/abs/2402.07927) — survey reference and taxonomy perspective.
- [Chain-of-Thought](https://arxiv.org/abs/2201.11903), [Self-Consistency](https://arxiv.org/abs/2203.11171), [Tree of Thoughts](https://arxiv.org/abs/2305.10601), [Graph of Thoughts](https://arxiv.org/abs/2308.09687), and [ReAct](https://arxiv.org/abs/2210.03629).
- [PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435), [Toolformer](https://arxiv.org/abs/2302.04761), and [Reflexion](https://arxiv.org/abs/2303.11366).
- [OpenAI: Working with evals](https://developers.openai.com/api/docs/guides/evals) and [Google: Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) — official implementation guidance.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — security risks that prompt patterns must not bypass.

### Additional references

- <https://arxiv.org/abs/2201.11903>
- <https://arxiv.org/abs/2205.10625>
- <https://arxiv.org/abs/2305.04091>
- <https://arxiv.org/abs/2203.11171>
- <https://arxiv.org/abs/2303.11366>
- <https://arxiv.org/abs/2305.10601>
- <https://arxiv.org/abs/2308.09687>
- <https://arxiv.org/abs/2210.03629>
- <https://arxiv.org/abs/2211.10435>
- <https://arxiv.org/abs/2302.04761>
- <https://arxiv.org/abs/2406.06608>
- <https://arxiv.org/abs/2402.07927>
- <https://developers.openai.com/api/docs/guides/evals>
- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- <https://genai.owasp.org/llm-top-10/>
