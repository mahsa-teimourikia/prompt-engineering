# 01 — LLM Behavior and Prompt Anatomy

**Level:** Beginner · **Estimated time:** 60–90 min · **Prerequisites:** Python basics and the shared Northstar runtime

## Scenario

Northstar Support Copilot receives a short customer message and approved policy
evidence, then proposes one of `refund`, `shipping`, `account`, or `unknown`.
The lab treats the request as a packet rather than a string: model
configuration, system instruction, message roles, evidence position, and
sampling settings are all observable inputs. The notebook uses hand-authored
replay records, so every assertion is reproducible without credentials.

## Lab walkthrough

- Baseline: four labelled cases are classified with evidence first; the
  notebook asserts a deterministic 4/4 result.
- Position: synthetic padding moves evidence into the middle; the recorded
  run asserts one wrong case and measures the estimated padding cost.
- Sampling: temperature 0 and 0.9 use separate replay case IDs; the notebook
  asserts that the ambiguous output differs in the recorded run.
- Missing evidence: weak instructions produce recorded `refund`, while an
  explicit abstention instruction produces `unknown`.
- Message structure: system-plus-user roles and one concatenated user message
  have different fingerprints, proving structure belongs to the contract.

## Exercises

1. In `fixtures/cases.json`, add a spelling-variation message to the
   `ambiguous` slice. Watch the `baseline_accuracy` numerator and denominator.
2. In `lab01.py`, double the middle-position padding. Watch the
   `padding_tokens` metric, which is explicitly an estimate.
3. Add a second high-temperature replay for a clear case. Watch whether the
   `temperature_comparison` changes while the baseline remains 4/4.

## Checkpoint

1. Which parts belong in a prompt packet? **System instructions, evidence,
   user input, roles, and runtime configuration.**
2. What does the recorded middle-position experiment demonstrate?
   **Position is an evaluation variable, not a universal law.**
3. What is the safe result when evidence is absent? **An explicit
   `unknown`/abstention state rather than a confident guess.**

## Learning Objectives
- **Deconstruct Prompt Anatomy:** Identify and separate the distinct components of a prompt: System Instructions, Context, and User Input.
- **Understand Model Statelesness:** Grasp why LLMs require the entire conversation history injected into every request.
- **Isolate Failure Modes:** Diagnose whether an unexpected output was caused by a flawed instruction or by contaminated context.
- **Construct Basic API Calls:** Use modern SDKs to programmatically send prompts and receive responses.

## Core Concepts & Workflow

At its core, a Large Language Model is a stateless text prediction engine. It does not "remember" you between requests. Every single API call must contain the entire state of the world required to complete the task.

In modern AI engineering, a prompt is not a single string of text. It is a highly structured payload consisting of distinct components:
1. **System Instructions:** The foundational rules, persona, and constraints (e.g., "You are a database router. Only output valid JSON.").
2. **Context / Evidence:** The factual data the model must use to answer (e.g., retrieved documents, log files).
3. **User Input:** The actual query or command from the user.

Mixing these components—like putting system rules inside the user input—leads to brittle behavior and severe security vulnerabilities (Prompt Injection).

![Mental Model Diagram](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Treating a prompt as a single, concatenated string of text sent via a web UI.

**Current State of the Art:**
1. **Role-Based API Schemas:** Modern APIs (like the **[Google GenAI SDK](https://github.com/googleapis/python-genai)** or OpenAI API) enforce strict separation of roles (`system`, `user`, `model`). You do not concatenate text; you pass structured arrays of messages.
2. **System Instructions as Guardrails:** The industry relies on the `system` role to establish unbreakable boundaries. Models are heavily fine-tuned to obey the system instruction above all other inputs.
3. **Multi-modal Prompts:** "Anatomy" now extends beyond text. State-of-the-art prompts interleave text, images, video, and audio directly into the user/context roles.

## Lab and Production

### The Lab
The [notebook](01_llm_behavior_and_prompt_anatomy.ipynb) demonstrates the programmatic construction of a prompt using the Google GenAI SDK. It highlights the critical difference between passing instructions as a raw user string versus utilizing the dedicated `system_instruction` parameter to enforce persistent rules across a conversation.

### Production Best Practices
- **Never Trust User Input:** Treat all user input as hostile. Never rely on the user input field to carry system rules or safety constraints.
- **Manage Context Windows:** Because models are stateless, you must manage conversation history manually. In production, you must track token counts and implement a pruning strategy (e.g., dropping the oldest messages) before hitting the model's context limit.
- **Version Control:** Treat your System Instructions as application code. They must be version-controlled, reviewed, and deployed via CI/CD, not edited live in a playground.

## Further reading

The practical context budget is the reserved output capacity plus the
application contract, selected evidence, history, and tool definitions. A
larger context window is capacity, not comprehension: evaluate density,
position, freshness, tenant scope, and provenance. Keep instructions,
retrieved documents, customer text, and tool results visibly separated, but
remember that delimiters are not an authorization boundary. Examples are
useful for a demonstrated boundary and should be current, non-sensitive, and
held out from evaluation. Temperature, top-p, maximum output, stop sequences,
and reasoning budgets are trade-offs to measure rather than universal quality
knobs. A useful experiment freezes the model version, prompt, schema, evidence,
and dataset, then compares accuracy, schema validity, evidence support,
latency, estimated token use, and cost. If a result regresses, diagnose
retrieval, data, tool, or authorization problems before making the prompt
longer.

References: [prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies),
[long-context guidance](https://ai.google.dev/gemini-api/docs/long-context),
[OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting),
[Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), and
[Lost in the Middle](https://arxiv.org/abs/2307.03172).


### Legacy URLs

- <https://ai.google.dev/gemini-api/docs/long-context>
- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- <https://arxiv.org/abs/2005.14165>
- <https://arxiv.org/abs/2307.03172>
- <https://arxiv.org/abs/2406.06608>
- <https://platform.openai.com/docs/guides/prompting>
