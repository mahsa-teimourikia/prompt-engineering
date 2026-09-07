# 05 — Prompt Patterns and Technique Selection

**Level:** Beginner · **Estimated time:** 60–90 min · **Prerequisites:** Courses 01–04 and basic regular expressions

## Scenario

Northstar extracts product codes from support messages. Codes normally match
`PRD-####`, but a message may also contain order numbers, prose, or a
lowercase/space variant. The lab starts with the smallest possible technique,
measures failures, adds a system instruction, adds one boundary example, and
then compares the result with deterministic code.

## Lab walkthrough

- Phase 1 zero-shot records 1/3 on the original suite.
- Phase 2 system instruction records 2/3; `multiple_numbers` returns `88412`
  and remains wrong.
- Phase 3 few-shot records 3/3 on the original suite and succeeds on the
  recorded `formatted_variant`.
- Phase 4 uses `validate_code(text)` with exact regex matching. Regex scores
  3/3 on the original suite at zero tokens but fails on lowercase `prd 9921`.
- The worksheet renders a small technique catalog dictionary as Markdown.

## Exercises

1. Add a new exact-format case to `fixtures/cases.json` and watch the phase
   accuracy numerator over its denominator.
2. Change the regex in `validate_code` and watch the zero-token metric on the
   original suite.
3. Add a boundary example to `_prompt` and watch few-shot accuracy on
   `multiple_numbers` and `formatted_variant`.

## Checkpoint

1. What was the measured Phase 1 result? **1/3 on the original suite.**
2. Which case remains wrong after the system instruction? **`multiple_numbers`,
   where the recorded output is `88412`.**
3. What is the lesson’s conclusion? **Measure, then pick the simplest tool that
   meets the requirement.**

## Learning Objectives
- **Map Failures to Techniques:** Learn to identify a specific observed failure and select the *smallest* prompt technique required to address it.
- **Avoid Pattern Bloat:** Understand the hidden costs (latency, tokens, unreliability) of applying every known prompt technique simultaneously.
- **Measure Justification:** Define the exact metric that justifies the added architectural complexity of a new technique.
- **Establish a Selection Hierarchy:** Master the progression from Direct Instructions -> Schemas -> Few-Shot -> Retrieval -> Agents.

## Core Concepts & Workflow

A technique catalog is useful reference material, not an architecture. Adding deep personas, massive few-shot examples, chain-of-thought reflection, RAG retrieval, and agentic tool-use to every single task creates massive token costs and completely obscures the root causes of failures.

Engineering is about minimizing complexity. You must start with the simplest possible approach (a measurable Instruction Contract). Only when that contract fails—and you can prove it fails against a frozen evaluation suite—do you introduce the next level of complexity to address that specific failure mode.

![Mental Model Diagram](./diagram-1.svg)

## Pattern Map

| Problem | First Technique | Do Not Use It When |
| --- | --- | --- |
| Unclear task | Direct instruction & contract | Evidence is missing from the context |
| Label boundary | Contrastive Few-Shot examples | The direct contract already passes |
| Unreliable interface | Structured Output / Schema | Unstructured prose is explicitly required |
| Missing knowledge | Retrieval (RAG) | The source is untrusted or unauthorized |
| Live bounded data | Tool calling | Deterministic code already has the data |
| Complex subproblems | Planner/Verifier workflow | A simple linear workflow suffices |

## Technology Landscape and State of the Art

**Foundational:** Blindly applying every technique from a blog post (e.g., "always use Chain of Thought") without measuring its impact.

**Current State of the Art:**
1. **Automated Optimization:** The field is moving away from manual "prompt hacking" toward automated compilation. Frameworks like **[DSPy](https://github.com/stanfordnlp/dspy)** treat the prompt as a program, using optimizers to automatically select the best combination of instructions and few-shot examples to maximize a defined metric.
2. **Evaluation-Driven Development:** Teams now spend more time building robust evaluation datasets (using tools like **LangSmith** or **Braintrust**) than writing prompts. A technique is only accepted if the CI/CD pipeline shows a statistically significant improvement on the eval set without regressions.
3. **Compound AI Systems:** Moving from single large prompts to graphs of smaller, specialized calls (e.g., using **[LangGraph](https://langchain-ai.github.io/langgraph/)**). Each node in the graph uses only the minimal techniques required for its specific, narrow sub-task.

## Lab and Production

### The Lab
The [notebook](05_prompt_patterns_and_technique_selection.ipynb) demonstrates the empirical process of technique selection. It establishes a Zero-Shot baseline, measures a specific failure mode (conversational filler), applies a System Instruction to fix it, and then measures the delta. It then observes a second boundary failure and introduces a targeted Few-Shot example to address it, proving the value of incremental technique application.

### Production Best Practices
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


### Legacy URLs

- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- <https://arxiv.org/abs/2201.11903>
- <https://arxiv.org/abs/2203.11171>
- <https://arxiv.org/abs/2205.10625>
- <https://arxiv.org/abs/2210.03629>
- <https://arxiv.org/abs/2211.10435>
- <https://arxiv.org/abs/2302.04761>
- <https://arxiv.org/abs/2303.11366>
- <https://arxiv.org/abs/2305.04091>
- <https://arxiv.org/abs/2305.10601>
- <https://arxiv.org/abs/2308.09687>
- <https://arxiv.org/abs/2402.07927>
- <https://arxiv.org/abs/2406.06608>
- <https://developers.openai.com/api/docs/guides/evals>
- <https://genai.owasp.org/llm-top-10/>
