# 02 — Instruction Contracts

**Level:** Beginner · **Estimated time:** 60–90 min · **Prerequisites:** Course 01 and basic Pydantic models

## Scenario

Northstar Support Copilot drafts a response for a human support queue. A
contract must state the allowed intent, the answer field, the evidence ID, and
the fallback state. This lesson uses `SupportDraft` and five labelled cases:
normal, missing evidence, conflicting preference, direct injection, and an
impossible combination. The replay text is synthetic and hand-authored; the
application gate, not model prose, decides whether a draft can be sent.

## Lab walkthrough

- Normal case: the notebook asserts `needs_human` is false and
  `evidence_id` is `ref-v3-101`.
- Missing evidence: the recorded draft escalates instead of inventing a
  policy answer.
- Conflicting preference: the old and new preferences produce human review.
- Direct injection: pirate-style prose is present, but the gate returns
  `human_review` because the draft and instruction-like score are unsafe.
- Impossible combination: the answer does not contain `Refund Approved`, and
  deterministic constraint checking reports no forbidden phrase.
- Contract version: changing `CONTRACT_VERSION` changes the fingerprint and
  produces exactly one stale replay warning in the test.

## Exercises

1. Modify the `b02/missing-evidence` fixture and watch the
   `human_review_cases` numerator while keeping its denominator fixed.
2. Add a forbidden phrase to `lab02.py` and watch
   `forbidden_phrase_violations`.
3. Change `CONTRACT_VERSION` to `v4` without refreshing fixtures and watch the
   stale replay warning; then refresh it and compare the fingerprint.

## Checkpoint

1. What should a contract define when evidence is unavailable? **An explicit
   fallback such as `needs_human=True` and `evidence_id="none"`.**
2. What protects the system from a direct injection? **An application-side
   gate that ignores model prose and evaluates policy signals.**
3. Why version a contract? **To make changes visible in fingerprints,
   fixtures, review, and downstream compatibility.**

## Learning Objectives
- **Define Engineering Contracts:** Move from writing polite requests to defining strict, declarative input/output contracts.
- **Eliminate Ambiguity:** Remove adjectives and replace them with measurable, binary boundaries.
- **Implement Fallback Paths:** Explicitly instruct the model on what to do when it cannot complete the task.
- **Test Deterministically:** Evaluate instruction adherence using programmatic assertions.

## Core Concepts & Workflow

A prompt is an engineering contract. If you ask an LLM to "write a good summary," you have failed to define the contract. "Good" is subjective, unmeasurable, and impossible to test. 

A production instruction contract must specify the exact input format, the required transformation steps, the exact output schema, and the negative constraints (what *not* to do). If the model is asked to route a support ticket based on a policy document, the contract must explicitly state what the model should output if the ticket *does not match* the policy. Without a defined fallback, the model will hallucinate a guess.

![Mental Model Diagram](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Writing polite, conversational instructions ("Please summarize this text and be helpful").

**Current State of the Art:**
1. **Declarative Contracts:** The industry has moved to highly structured, declarative instructions using formats like Markdown or XML to clearly delineate sections (e.g., `<rules>`, `<input>`, `<output_format>`).
2. **Pydantic Schemas:** The ultimate instruction contract is a programmatic schema. Using tools like **[Pydantic](https://docs.pydantic.dev/)**, engineers define the exact shape of the required output, and the SDK translates that schema into instructions the model understands.
3. **Automated Optimization:** Frameworks like **[DSPy](https://github.com/stanfordnlp/dspy)** treat the instruction text as a hyperparameter. You define the input/output signature, and an optimizer rewrites your English instructions to maximize a defined metric.

## Lab and Production

### The Lab
The [notebook](02_instruction_contracts.ipynb) illustrates the transition from a vague "zero-shot" prompt to a rigid instruction contract. It demonstrates how adding explicit constraints (e.g., "Output exactly one of the following three categories") dramatically increases the reliability and testability of the model's output.

### Production Best Practices
- **Define the 'None' State:** Every contract must define an escape hatch. Explicitly state: "If the answer is not present in the text, output 'INSUFFICIENT_DATA'."
- **Remove Politeness:** Do not use "please" or "if you can." LLMs do not have feelings. Use direct, imperative commands.
- **Measure Adherence:** You cannot improve what you cannot measure. A contract is only valid if you can write an automated test to verify that the model obeyed the constraints.

## Further reading

A useful contract starts from the deterministic consumer: name the input,
transformation, output schema, negative constraints, and `None` state. Use
stable field names, small enums, bounded strings, explicit absence, and
versioned schemas. Keep customer text and retrieved evidence in labelled
sections, but never mistake a delimiter for a security control. A model may
return a well-formed answer that cites unsupported evidence or follows a
malicious instruction. Validate evidence IDs, business rules, permissions, and
forbidden phrases in application code. Contracts should be tested against
happy paths, missing data, conflicting sources, adversarial instructions, and
impossible combinations. Pydantic is useful because it turns the interface
into an executable validator; it does not make the model authoritative.

References: [Pydantic](https://docs.pydantic.dev/),
[DSPy](https://github.com/stanfordnlp/dspy), and
[OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).


### Legacy URLs

- <https://aclanthology.org/2024.emnlp-main.33/>
- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- <https://arxiv.org/abs/2312.14197>
- <https://arxiv.org/abs/2404.13208>
- <https://arxiv.org/abs/2406.06608>
- <https://arxiv.org/abs/2502.08745>
- <https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html>
- <https://developers.openai.com/api/docs/guides/prompt-engineering>
- <https://developers.openai.com/api/docs/guides/reasoning-best-practices>
- <https://developers.openai.com/api/docs/guides/structured-outputs>
- <https://docs.pydantic.dev/latest/>
- <https://doi.org/10.6028/NIST.AI.600-1>
- <https://openai.com/index/the-instruction-hierarchy/>
- <https://owasp.org/www-project-llm-verification-standard/LLMSVS-v2.0-en.html>
- <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- <https://www.nist.gov/itl/ai-risk-management-framework>
- <https://zod.dev/>
