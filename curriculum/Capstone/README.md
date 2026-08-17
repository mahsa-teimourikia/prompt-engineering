# Capstone: Project Northstar

Welcome to the **Project Northstar: Enterprise Support Copilot** capstone!

In this project, you will build a complete, production-ready AI Agent incrementally. Instead of isolated exercises, you will progress through 5 milestones that force you to combine the skills learned across the Beginner, Intermediate, Advanced, and Enterprise tracks.

## The Sequence

1. **[Milestone 1: The Foundation](01_milestone_foundation.ipynb)**
   - **Concepts:** Pydantic I/O Contracts, Zero-Shot Prompting, Instruction Engineering.
   - **Goal:** Ingest raw customer emails and extract structured `intent`, `urgency`, and `sentiment`.

2. **[Milestone 2: Context & Action](02_milestone_rag_and_tools.ipynb)**
   - **Concepts:** Retrieval-Augmented Generation (RAG), Function Calling (Tools).
   - **Goal:** Connect the Copilot to a simulated Knowledge Base and a `get_order_status` database tool.

3. **[Milestone 3: Security & Multi-Agent Routing](03_milestone_routing_and_security.ipynb)**
   - **Concepts:** Semantic Routing, Prompt Security, Prompt Injection Defenses.
   - **Goal:** Build a router to classify safe vs. unsafe queries, and route technical questions to a specialized sub-agent.

4. **[Milestone 4: Portability & Fallbacks](04_milestone_portability.ipynb)**
   - **Concepts:** Model Adapters, Fallback Strategies.
   - **Goal:** Abstract your LLM calls behind an adapter that automatically falls back to a secondary model if the primary model fails or violates a contract.

5. **[Milestone 5: Production Release Gate](05_milestone_production_release.ipynb)**
   - **Concepts:** Evaluators, Observability, Release Engineering.
   - **Goal:** Wrap the system in simulated OpenTelemetry spans, evaluate it against a golden dataset, and generate a final Architecture Decision Record (ADR).
