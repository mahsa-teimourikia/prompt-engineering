# Curated resource library: state of the art, with a learning path

## How to use this library

This is a curated map, not a prompt dump. Start with the course's guided modules and Northstar notebooks; use this page to go deeper into a technique, select an evaluation benchmark, or verify fast-changing provider capabilities. Labels mean:

- **Foundational** — durable concept or original paper learners should understand.
- **Practical** — commonly useful engineering pattern or maintained documentation.
- **Emerging** — useful research direction; validate before treating it as production-default.
- **Vendor-specific** — current implementation guidance; verify model/version behavior before use.

## 1. Foundations and broad surveys

| Resource | Label | Why it belongs here |
| --- | --- | --- |
| [The Prompt Report](https://arxiv.org/abs/2406.06608) | Foundational | Broad taxonomy of text and multimodal prompting techniques; use it to orient terminology. |
| [A Systematic Survey of Prompt Engineering](https://arxiv.org/abs/2402.07927) | Foundational | Links techniques to applications and research literature. |
| [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) | Foundational | Landmark work on in-context learning and demonstrations. |
| [A Survey of Context Engineering for LLMs](https://arxiv.org/abs/2507.13334) | Emerging | Large survey covering retrieval, processing, memory, tools, and multi-agent context. |
| [Lost in the Middle](https://arxiv.org/abs/2307.03172) | Foundational | Shows why a large context window should not be treated as uniform comprehension. |

## 2. Prompting and reasoning techniques

Read these alongside [the technique catalog](14-technique-catalog.md) and [reasoning module](11-reasoning-techniques.md).

| Resource | Label | Study question |
| --- | --- | --- |
| [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) | Foundational / model-dependent | When do intermediate-reasoning demonstrations help, and what is their cost? |
| [Self-Consistency](https://arxiv.org/abs/2203.11171) | Foundational | When does multiple-sample aggregation improve a verifiable task enough to justify latency? |
| [Least-to-Most Prompting](https://arxiv.org/abs/2205.10625) | Foundational | How can subproblem ordering help compositional reasoning? |
| [Take a Step Back](https://arxiv.org/abs/2310.06117) | Practical / model-dependent | Does abstraction before solving improve the task at hand? Test it. |
| [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091) | Practical / model-dependent | Does explicit planning reduce missing-step errors for this workflow? |
| [Tree of Thoughts](https://arxiv.org/abs/2305.10601) | Emerging | Explore, score, and prune alternatives only when search quality can be evaluated. |
| [Graph of Thoughts](https://arxiv.org/abs/2308.09687) | Emerging | Non-linear reasoning structures; compare against simpler decomposition first. |
| [Reflexion](https://arxiv.org/abs/2303.11366) and [Self-Refine](https://arxiv.org/abs/2303.17651) | Practical / model-dependent | Generate–feedback–refine patterns; guard against correlated self-critique. |
| [Directional Stimulus Prompting](https://arxiv.org/abs/2302.11520) | Emerging | Use controlled hints; do not treat them as evidence. |
| [Active-Prompt](https://arxiv.org/abs/2302.12246) | Emerging | Choose examples based on uncertainty; preserve safety/edge-case coverage. |
| [PAL: Program-Aided Language Models](https://arxiv.org/abs/2211.10435) | Practical | Let deterministic code execute calculations while the model interprets the result. |

## 3. RAG, context, knowledge, and citations

| Resource | Label | What to learn |
| --- | --- | --- |
| [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | Foundational | Original retrieve-then-generate framing. |
| [HyDE](https://arxiv.org/abs/2212.10496) | Practical / model-dependent | Hypothetical-document query expansion; evaluate retrieval improvement and hallucination risk. |
| [Self-RAG](https://arxiv.org/abs/2310.11511) | Emerging | Retrieve/generate/critique behavior with self-reflection tokens. |
| [CRAG](https://arxiv.org/abs/2401.15884) | Emerging | Corrective retrieval and confidence-aware handling. |
| [RAGAS](https://arxiv.org/abs/2309.15217) | Practical | Reference-free RAG evaluation signals; calibrate against human review. |
| [RAGTruth](https://arxiv.org/abs/2401.00396) | Practical | Hallucination benchmark/data for RAG systems. |

Use [the Awesome RAG Learning Hub](https://mahsa-teimourikia.github.io/awsome-rag/) for a complete retrieval-system curriculum; this course focuses on the prompt/context interface to RAG.

## 4. Tools, workflows, and agents

| Resource | Label | What to learn |
| --- | --- | --- |
| [ReAct](https://arxiv.org/abs/2210.03629) | Foundational | Reason → act → observe loop that connects prompting to tool use. |
| [Toolformer](https://arxiv.org/abs/2302.04761) | Foundational | Tool-use learning and API interaction framing. |
| [ART: Automatic Reasoning and Tool-use](https://arxiv.org/abs/2303.09014) | Emerging | Retrieve tool-use programs for multi-step work. |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Practical | Prefer simple composable workflows over unnecessary autonomy. |
| [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/) | Vendor-specific | Managed agents, tools, handoffs, guardrails, sessions, and tracing. |
| [LangGraph documentation](https://langchain-ai.github.io/langgraph/) | Practical | Explicit state graphs, persistence, and human approval. |
| [AutoGen](https://microsoft.github.io/autogen/) and [CrewAI](https://docs.crewai.com/) | Practical | Compare conversation/team versus role/task mental models. |
| [GAIA benchmark](https://arxiv.org/abs/2311.12983) | Practical | General assistant evaluation across reasoning, web, tools, and multimodality. |
| [τ-bench](https://arxiv.org/abs/2406.12045) | Practical | Stateful tool-agent-user interaction and policy following. |

## 5. Evaluation, observability, and optimization

| Resource | Label | What to learn |
| --- | --- | --- |
| [OpenAI Evals](https://platform.openai.com/docs/guides/evals) | Vendor-specific | Dataset/rubric design and evaluation workflow. |
| [OpenAI Evals open-source framework](https://github.com/openai/evals) | Practical | Example evaluators and registry patterns. |
| [G-Eval](https://arxiv.org/abs/2303.16634) | Foundational | Rubric-driven LLM judging; calibrate before trusting it. |
| [TruthfulQA](https://arxiv.org/abs/2109.07958) | Foundational | Truthfulness and imitation of common falsehoods. |
| [DSPy](https://arxiv.org/abs/2310.03714) | Practical | Evaluation-driven optimization of LM programs. |
| [Promptfoo](https://www.promptfoo.dev/docs/intro/) | Practical | Multi-provider evals, red teaming, and CI integration. |
| [LangSmith](https://docs.smith.langchain.com/) | Practical | Tracing, datasets, and evaluations. |
| [Arize Phoenix](https://docs.arize.com/phoenix) | Practical | Open-source observability/evaluation for LLM applications. |

## 6. Safety, security, governance, and human oversight

| Resource | Label | What to learn |
| --- | --- | --- |
| [OWASP Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | Practical | Direct/indirect injection, RAG poisoning, tool manipulation, and defense in depth. |
| [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | Practical | Agent identity, permissions, approvals, audit metadata, and runtime controls. |
| [OWASP Secure AI Model Ops](https://cheatsheetseries.owasp.org/cheatsheets/Secure_AI_Model_Ops_Cheat_Sheet.html) | Practical | Operating/deploying AI systems securely. |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) and [Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Practical | Risk framing, governance, roles, measurement, and lifecycle controls. |
| [Sycophantic Behaviour in LLMs](https://arxiv.org/abs/2311.09410) | Foundational | Why agreement with a user premise is not evidence. |

## 7. Provider documentation: verify before you build

Provider capability and API behavior changes quickly. Use official documentation for current model limits, pricing, retention, tool semantics, structured-output support, and safety policies:

- [OpenAI prompting](https://platform.openai.com/docs/guides/prompting), [structured outputs](https://platform.openai.com/docs/guides/structured-outputs), [function calling](https://platform.openai.com/docs/guides/function-calling), and [safety best practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Anthropic documentation](https://docs.anthropic.com/), [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and [effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Gemini prompting](https://ai.google.dev/gemini-api/docs/prompting-strategies), [structured output](https://ai.google.dev/gemini-api/docs/structured-output), [function calling](https://ai.google.dev/gemini-api/docs/function-calling), and [long context](https://ai.google.dev/gemini-api/docs/long-context)

## Resource selection checklist

Before adopting a resource or framework, ask: Is it maintained? Does it solve the measured failure? Does it preserve evidence/tenant boundaries? Can it export traces and evaluation artifacts? What new cost, latency, or attack surface does it introduce? Is there a simpler baseline to compare?

The most useful resource is the one that improves a measured system outcome—not the newest technique in a catalog.
