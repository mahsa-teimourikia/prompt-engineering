# Prompt Engineering Learning Hub

> Design reliable AI behavior with clear instructions, deliberate context, typed outputs, evidence, evaluation, and guardrails.

[**Open the Prompt Engineering Learning Hub →**](https://mahsa-teimourikia.github.io/prompt-engineering/)
 · [Knowledge check](https://mahsa-teimourikia.github.io/prompt-engineering/quiz/)

![Prompt engineering trends: from prompt crafting to AI system engineering](assets/prompt-engineering-trends.png)

## What is prompt engineering?

Prompt engineering is the disciplined design, testing, and improvement of the instructions and context that guide a model toward a useful result. A production prompt is not a magic phrase: it is a **behavior contract**. It states the task, supplies the relevant evidence, constrains unsafe or unsupported behavior, and asks for a result that software and people can verify.

Modern practice increasingly includes **context engineering**: selecting and structuring the right instructions, user state, retrieved evidence, tool definitions, tool results, and conversation history for a particular decision. Better wording cannot compensate for missing evidence, unsafe tools, or an unmeasured failure mode.

This curriculum follows the evolution from **prompt crafting → prompt engineering → reasoning engineering → context engineering → tool and workflow engineering → agent prompt engineering → evaluation-driven optimization → PromptOps → AI system engineering**. Prompt engineering did not become irrelevant; it became one measurable layer of a larger behavior system. The core framework is:

`Prompt + model + context + examples + retrieval + tools + state + policies + evaluation + runtime configuration = dependable AI behavior`

## Start in the Learning Hub

The [Learning Hub](https://mahsa-teimourikia.github.io/prompt-engineering/) is the structured starting point. Choose a level, select a lesson, then use its **Learn**, **Notebook**, and **Checkpoint** tabs. The hub links to each self-contained notebook, source material, and focused quiz question. Your completion status stays in your browser.

## Curriculum roadmap

The repository is being migrated in deliberate phases; it does **not** claim that all target lessons have already been generated. The current published lessons remain available in the Hub while the canonical structure is built and validated topic by topic. See the [curriculum evolution plan](CURRICULUM_EVOLUTION_PLAN.md) for the audit, source-material disposition, implementation sequence, and complete mapping.

| Level | Canonical sequence | Current focus |
| --- | --- | --- |
| Beginner | 01–05: behavior, contracts, examples, typed interfaces, technique selection | Turn ambiguous support requests into validated case briefs. |
| Intermediate | 06–13: reasoning, workflows, context, conversations, RAG, tools, multimodality, security | Build evidence- and tool-grounded systems with explicit trust boundaries. |
| Advanced | 14–21: evaluation, judges, optimization, agents, coding, models, efficiency | Improve behavior only when a measured evaluation supports the change. |
| Production | 22–29: PromptOps, observability, release engineering, governance, trust, portability, architecture, capstone | Ship, diagnose, govern, and roll back an AI behavior artifact. |

The notebooks share the **Northstar Support Copilot** scenario. They help support specialists answer order, billing, and product-policy questions. The scenario deliberately includes conflicting evidence, injection-like content, strict schemas, and evaluation cases—conditions that make trade-offs visible without requiring credentials.

The course distinguishes **foundational** practices (clear task contracts, schemas, context, and evaluation), **practical** practices (boundary examples, evidence grounding, narrow tools, and PromptOps), **model-dependent** rituals (for example blanket personas or verbose chain-of-thought requests), and **emerging** practices (automatic optimization and learned context policies). The [current coverage map](docs/20-course-coverage-map.md) remains available during the migration.

## Run locally

```bash
git clone https://github.com/mahsa-teimourikia/prompt-engineering.git
cd prompt-engineering
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
jupyter lab
```

Run the self-contained notebooks with `make notebooks`, or run `pytest` to validate notebook coverage and quiz data. Provider calls are optional and deliberately absent from the default execution path.

## Current published learning material

The following is the current, fully linked library. As each target course is completed, the Hub registry and this section will be re-ordered into the canonical 29-course path. Reference-oriented material is intentionally separated below rather than presented as a required advanced skill.

Canonical migration is underway: [Course 01 — LLM Behavior and Prompt Anatomy](curriculum/beginner/01-llm-behavior-and-prompt-anatomy/README.md), [Course 02 — Instruction Contracts](curriculum/beginner/02-instruction-contracts/README.md), and [Course 03 — Constraints, Examples, and Few-Shot Learning](curriculum/beginner/03-constraints-examples-and-few-shot-learning/README.md) each include a guided notebook and reusable offline lab. The original Modules 18, 01, and 02 remain available as legacy supporting material while later courses migrate.

### Beginner — define behavior before generation

1. [Instruction contracts and prompting foundations](docs/01-instruction-contracts.md) · [Self-contained notebook](notebooks/01_instruction_contracts.ipynb)
2. [Examples, constraints, and structured output](docs/02-structured-outputs.md) · [Self-contained notebook](notebooks/02_structured_outputs.ipynb)
3. [Context engineering and grounded answers](docs/03-context-engineering.md) · [Self-contained notebook](notebooks/03_context_engineering.ipynb)

### Intermediate — connect prompts to evidence and systems

4. [RAG and tool-use prompt interfaces](docs/04-rag-tools.md) · [Self-contained notebook](notebooks/04_rag_and_tools.ipynb)
5. [Multimodal document prompting](docs/05-multimodal.md) · [Self-contained notebook](notebooks/05_multimodal_prompting.ipynb)
6. [Prompt injection, privacy, and tool boundaries](docs/06-prompt-security.md) · [Self-contained notebook](notebooks/06_prompt_security.ipynb)
7. [Evaluation and prompt experiments](docs/07-evaluation.md) · [Self-contained notebook](notebooks/07_prompt_evaluation.ipynb)

### Advanced and production foundations — engineer reliable systems, not isolated prompts

8. [Agent and multi-agent prompt contracts](docs/08-agentic-prompts.md) · [Self-contained notebook](notebooks/08_agentic_prompts.ipynb)
9. [PromptOps release engineering](docs/09-promptops.md) · [Self-contained notebook](notebooks/09_promptops.ipynb)
11. [Reasoning-oriented prompting: decomposition, verification, and search](docs/11-reasoning-techniques.md) · [Self-contained notebook](notebooks/11_reasoning_techniques.ipynb)
12. [Prompt engineering for coding agents](docs/12-coding-agent-prompting.md) · [Self-contained notebook](notebooks/12_coding_agent_prompting.ipynb)
13. [Prompt cost and latency engineering](docs/13-cost-latency-engineering.md) · [Self-contained notebook](notebooks/13_cost_latency_engineering.ipynb)
16. [Model-aware guidance](docs/16-model-aware-guidance.md) · [Self-contained notebook](notebooks/16_model_aware_guidance.ipynb)
18. [LLM behavior, sampling, and prompt structure](docs/18-llm-behavior-and-prompt-structure.md) · [Self-contained notebook](notebooks/18_llm_behavior_prompt_structure.ipynb)
19. [Reliability and human-centred AI](docs/19-reliability-and-human-centred-ai.md) · [Self-contained notebook](notebooks/19_reliability_human_centred_ai.ipynb)
21. [Evaluation-driven prompt optimization](docs/21-evaluation-driven-prompt-optimization.md) · [Self-contained notebook](notebooks/21_evaluation_driven_prompt_optimization.ipynb)

## Supporting reference material

These useful resources are retained as supporting material during the migration; they are not canonical completion requirements.

- [Technology landscape](docs/10-technology-review.md) · [notebook](notebooks/10_technology_review.ipynb)
- [Prompt technique catalog](docs/14-technique-catalog.md) · [notebook](notebooks/14_technique_catalog.ipynb)
- [Application playbooks](docs/15-application-playbooks.md) · [notebook](notebooks/15_application_playbooks.ipynb)
- [Curated resource library](docs/17-resource-library.md) · [notebook](notebooks/17_resource_library.ipynb)
- [Current coverage map](docs/20-course-coverage-map.md) · [notebook](notebooks/20_course_coverage_map.ipynb)

## Technology and state of the art

The course treats vendor frameworks as tools, not the curriculum. Use a model provider's prompt guide for model-specific details; use **JSON Schema/Pydantic** for contracts; **DSPy** or equivalent optimizers only after establishing an evaluation set; and an eval/tracing platform when prompt changes need release governance. For agents, tool descriptions and permission checks are part of the prompt interface, but authorization remains application code.

See [Technology review](docs/10-technology-review.md) for decision guidance covering OpenAI, Anthropic, Google Gemini, open-source structured-generation libraries, DSPy, LangSmith, Promptfoo, Phoenix, and evaluation approaches.

## Curated references

- [The Prompt Report — systematic survey of prompting techniques](https://arxiv.org/abs/2406.06608)
- [A systematic survey of prompt engineering](https://arxiv.org/abs/2402.07927)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903), [ReAct](https://arxiv.org/abs/2210.03629), and [Toolformer](https://arxiv.org/abs/2302.04761)
- [Anthropic: effective context engineering for agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and [building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Google prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting), [structured outputs](https://platform.openai.com/docs/guides/structured-outputs), and [evals](https://platform.openai.com/docs/guides/evals)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

## Contributing

Contributions should add a cited explanation, a credential-free executable notebook section, an experiment, and an evaluation or checkpoint. Please open an issue before introducing a provider-specific dependency.

Learning with [One+i](https://oneplusi.io) · responsible AI, real-world impact.
