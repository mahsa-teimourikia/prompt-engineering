# Prompt Engineering Learning Hub

> Design reliable AI behavior with clear instructions, deliberate context, typed outputs, evidence, evaluation, and guardrails.

[**Open the Prompt Engineering Learning Hub →**](https://mahsa-teimourikia.github.io/prompt-engineering/)
 · [Knowledge check](https://mahsa-teimourikia.github.io/prompt-engineering/quiz/)

![Prompt engineering trends: from prompt crafting to AI system engineering](assets/prompt-engineering-trends.png)

## What is prompt engineering?

Prompt engineering is the disciplined design, testing, and improvement of the instructions and context that guide a model toward a useful result. A production prompt is not a magic phrase: it is a **behavior contract**. It states the task, supplies the relevant evidence, constrains unsafe or unsupported behavior, and asks for a result that software and people can verify.

Modern practice increasingly includes **context engineering**: selecting and structuring the right instructions, user state, retrieved evidence, tool definitions, tool results, and conversation history for a particular decision. Better wording cannot compensate for missing evidence, unsafe tools, or an unmeasured failure mode.

This course follows the evolution from prompt → context → tools → agentic systems → evaluated, governed PromptOps. The core framework is:

`Task + context + constraints + examples + output contract + evaluation = dependable AI behavior`

## Start in the Learning Hub

The [Learning Hub](https://mahsa-teimourikia.github.io/prompt-engineering/) is the structured starting point. Choose a level, select a lesson, then use its **Learn**, **Lab**, and **Checkpoint** tabs. The hub links to each self-contained notebook, deterministic Python lab, source material, and focused quiz question. Your completion status stays in your browser.

## Learning roadmap

| Level | Focus | Scenario outcome |
| --- | --- | --- |
| Beginner | instruction contracts, examples, structured outputs, context | Turn ambiguous support requests into validated case briefs. |
| Intermediate | evidence, tools, multimodality, safety, evaluation | Build a grounded support copilot that retrieves policy evidence safely. |
| Advanced | agent policies, optimization, model-aware PromptOps | Ship an observable, versioned, tested prompt system with release gates. |

The labs share the **Northstar Support Copilot** scenario. It helps support specialists answer order, billing, and product-policy questions. The scenario deliberately includes conflicting evidence, injection-like content, strict schemas, and evaluation cases—conditions that make trade-offs visible without requiring credentials.

## Run locally

```bash
git clone https://github.com/mahsa-teimourikia/prompt-engineering.git
cd prompt-engineering
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
jupyter lab
```

Run deterministic labs with `python labs/01_instruction_contracts.py`, or run `pytest` to validate fixtures and quiz data. Provider calls are optional and deliberately absent from the default execution path.

## Course material

### Beginner — define behavior before generation

1. [Instruction contracts and prompting foundations](docs/01-instruction-contracts.md) · [Notebook](notebooks/01_instruction_contracts.ipynb) · [Lab](labs/01_instruction_contracts.py)
2. [Examples, constraints, and structured output](docs/02-structured-outputs.md) · [Notebook](notebooks/02_structured_outputs.ipynb) · [Lab](labs/02_structured_outputs.py)
3. [Context engineering and grounded answers](docs/03-context-engineering.md) · [Notebook](notebooks/03_context_engineering.ipynb) · [Lab](labs/03_context_engineering.py)

### Intermediate — connect prompts to evidence and systems

4. [RAG and tool-use prompt interfaces](docs/04-rag-tools.md) · [Notebook](notebooks/04_rag_and_tools.ipynb) · [Lab](labs/04_rag_and_tools.py)
5. [Multimodal document prompting](docs/05-multimodal.md) · [Notebook](notebooks/05_multimodal_prompting.ipynb) · [Lab](labs/05_multimodal_prompting.py)
6. [Prompt injection, privacy, and tool boundaries](docs/06-prompt-security.md) · [Notebook](notebooks/06_prompt_security.ipynb) · [Lab](labs/06_prompt_security.py)
7. [Evaluation and prompt experiments](docs/07-evaluation.md) · [Notebook](notebooks/07_prompt_evaluation.ipynb) · [Lab](labs/07_prompt_evaluation.py)

### Advanced — engineer reliable systems, not isolated prompts

8. [Agent and multi-agent prompt contracts](docs/08-agentic-prompts.md) · [Notebook](notebooks/08_agentic_prompts.ipynb) · [Lab](labs/08_agentic_prompts.py)
9. [Optimization, model-aware prompts, and PromptOps](docs/09-promptops.md) · [Notebook](notebooks/09_promptops_capstone.ipynb) · [Lab](labs/09_promptops_capstone.py)

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

Contributions should add a cited explanation, a credential-free executable example, a notebook experiment, and an evaluation or checkpoint. Please open an issue before introducing a provider-specific dependency.

Learning with [One+i](https://oneplusi.io) · responsible AI, real-world impact.
