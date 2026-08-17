# 18 — Agent and Multi-Agent Prompt Contracts

## Learning Objectives
- **Deconstruct God Prompts:** Break down monolithic, unreliable prompts into narrowly scoped specialist agents.
- **Enforce Contracts:** Use Pydantic schemas to strictly enforce the inputs and outputs between agents.
- **Build Supervisor Architectures:** Design state-machine-driven orchestrators that route tasks to specialists.
- **Maintain Tenant Boundaries:** Ensure that multi-agent systems respect authorization, idempotency, and security constraints at runtime.

## Core Concepts & Workflow

Early prompt engineering relied on "God Prompts"—massive walls of text commanding a single LLM to handle everything from database queries to customer chatting. These are brittle, impossible to test, and highly susceptible to prompt injection.

The modern approach is Multi-Agent Systems. Complex tasks are broken down into narrowly constrained "Specialist Agents," overseen by a central "Supervisor Agent." Crucially, these agents do not communicate via fuzzy English chat. They communicate via strict programmatic contracts (usually JSON constrained by Pydantic schemas). The Supervisor isn't told to "talk to the Database Agent"; it is given a tool that explicitly requires it to generate a valid `DatabaseQuerySchema` before the handoff occurs.

## Technology Landscape and State of the Art

**Foundational:** Trying to write one massive "God Prompt" that instructs a single LLM to handle everything from database queries to customer chat.

**Current State of the Art:** 
1. **Multi-Agent Systems:** Complex tasks are broken down into narrow, highly constrained "Specialist Agents" orchestrated by a central "Supervisor Agent". Frameworks like **[LangGraph](https://langchain-ai.github.io/langgraph/)**, **[Microsoft AutoGen](https://microsoft.github.io/autogen/)**, and **[CrewAI](https://www.crewai.com/)** are leading the industry in state-machine-driven agent orchestration.
2. **Contracts over Prompts:** The boundaries between these agents are not defined by fuzzy English instructions, but by strict programmatic contracts, usually enforced via **[Pydantic](https://docs.pydantic.dev/)**. The Supervisor isn't told "talk to the Database Agent," it is given a tool that *requires* it to generate a valid `DatabaseQuerySchema` JSON payload before the handoff can occur.

## Lab and Production

### The Lab
The [notebook](18_agent_and_multi_agent_prompt_contracts.ipynb) demonstrates a multi-agent Supervisor/Specialist pattern using the Google GenAI SDK. It highlights how to enforce rigid handoffs using Pydantic contracts rather than relying on unstructured LLM chat to coordinate complex logic.

### Production Best Practices
- **Minimize Autonomy:** Extra autonomy must demonstrate measured benefit. Do not use an agent if a simple `if/else` deterministic router will suffice.
- **Runtime Policies:** Prompts describe a role; runtime policy enforces identity. The LLM must not be responsible for enforcing tenant boundaries, authorization, or idempotency.
- **Idempotency:** Agent actions (tool calls) must be idempotent, as LLMs will frequently retry or loop instructions.
