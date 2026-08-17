# 28 — Prompt Architecture Patterns and System Selection

## Learning Objectives
- **Evaluate Architecture Trade-offs:** Systematically compare Zero-Shot, Few-Shot, RAG, Tool Use, and Agentic workflows.
- **Minimize Complexity:** Adhere to the principle that complexity is a liability; always select the simplest pattern that solves the problem.
- **Design for Scale:** Understand how different prompt architectures impact latency, token cost, and parallelization.
- **Map Business Constraints to AI Patterns:** Align strict regulatory or UX requirements with the appropriate technical architecture.

## Core Concepts & Workflow

There is no single "best" prompt architecture. A sprawling, multi-agent framework is a disaster for a simple classification task, and a basic Zero-Shot prompt will fail a complex data-synthesis task.

Engineering is about trade-offs. Every time you move up the complexity ladder (Code -> Prompt -> Schema -> Few-Shot -> RAG -> Tools -> Agents), you increase latency, increase token costs, and decrease determinism. System Selection is the practice of rigorously defining your business constraints (e.g., "Must respond in under 500ms," "Must cite sources," "Must cost less than $0.01 per query") and choosing the *simplest possible architecture* that meets those constraints.

![Architecture Selection Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Assuming every AI problem requires a massive, conversational "Agent."

**Current State of the Art:**
1. **Compound AI Systems:** The industry consensus has shifted from "One massive LLM solves everything" to Compound Systems. These systems mix deterministic code, simple classifier LLMs, and heavy reasoning LLMs in a single pipeline.
2. **Semantic Routing:** SOTA architectures use fast, cheap models (or even traditional NLP embeddings) to classify the user's intent *first*, and then route the query to the appropriate architecture (e.g., routing a casual chat to a fast model, but routing a complex data request to a heavy RAG pipeline).
3. **Serverless AI Execution:** Frameworks like **Modal** or **Baseten** allow engineers to deploy these complex, multi-stage AI workflows as serverless functions, scaling specific nodes of the architecture independently.

## Lab and Production

### The Lab
The [notebook](28_prompt_architecture_patterns_and_system_selection.ipynb) serves as an architectural design review. It presents a series of complex business problems and walks through the empirical process of selecting the right architecture. It demonstrates how to establish a baseline with a simple prompt, measure its failure, and justify the transition to a more complex pattern (like RAG or Tools) based on metrics.

### Production Best Practices
- **Default to Determinism:** If a problem can be solved with Regex, a SQL query, or a standard Python script, *do not use an LLM*.
- **The Complexity Tax:** Remember that adding an Agent or a self-reflection loop essentially multiplies your latency by 3x or more. Never introduce these patterns in synchronous, user-facing critical paths unless absolutely necessary.
- **Document Architectural Decisions (ADRs):** When choosing to implement a complex RAG system over a simple Few-Shot prompt, write an Architectural Decision Record explicitly documenting the evaluation metrics that proved the simpler system was insufficient.
