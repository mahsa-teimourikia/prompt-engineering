# 07 — Task Decomposition and Workflow Prompting

## Learning Objectives
- **Break Down Complex Tasks:** Deconstruct a massive, multi-step prompt into a pipeline of narrow, specialized prompts.
- **Design State Machines:** Orchestrate data flow between models using explicit programmatic states.
- **Implement Verification Gates:** Build steps that double-check the output of previous steps before proceeding.
- **Mitigate Compounding Errors:** Prevent hallucinations early in a pipeline from destroying the final output.

## Core Concepts & Workflow

LLMs struggle with long lists of complex instructions (e.g., "Read this 100-page document, extract all names, format them as XML, cross-reference them with this other document, and then write a summary"). When given too many tasks at once, models suffer from "attention dilution" and will silently skip instructions.

The solution is Task Decomposition. Instead of one massive prompt, you build a workflow of smaller, highly constrained prompts. 
1. **Model A** extracts the names.
2. **Model B** cross-references the list.
3. **Model C** writes the summary.
By separating the concerns, you can use smaller, faster models for simple steps, apply programmatic verification between steps, and isolate failures to specific nodes in your pipeline.

![Workflow Prompting](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Writing one massive prompt with 20 bullet points of instructions and hoping the model follows them all.

**Current State of the Art:**
1. **Graph-Based Orchestration:** Frameworks like **[LangGraph](https://langchain-ai.github.io/langgraph/)** model complex LLM workflows as state machines (graphs). Each node is a specific prompt or function, and edges determine the conditional routing based on the output.
2. **Multi-Agent Frameworks:** Tools like **[CrewAI](https://www.crewai.com/)** and **[Microsoft AutoGen](https://microsoft.github.io/autogen/)** formalize decomposition by assigning specific "personas" and "tools" to distinct agents that collaborate to solve the decomposed tasks.
3. **Map-Reduce Patterns:** For massive documents, state-of-the-art workflows use Map-Reduce: splitting the document into chunks, summarizing each chunk in parallel, and then passing the summaries to a final "Reduce" model.

## Lab and Production

### The Lab
The [notebook](07_task_decomposition_and_workflow_prompting.ipynb) demonstrates decomposing a complex summarization and extraction task. Instead of asking a single model to do everything, it chains together three separate Google GenAI SDK calls, passing the structured output of step 1 directly into the context of step 2.

### Production Best Practices
- **Beware Latency:** Chaining 5 model calls together means the user waits for 5 sequential network requests. Use streaming where possible, or use parallelization for independent sub-tasks.
- **Programmatic Glue:** Do not use an LLM to route data between steps if a simple Python `if/else` statement will work. 
- **Graceful Degradation:** If step 2 in a 5-step pipeline fails, the system should catch the error and either retry safely or return a clear error to the user, rather than passing hallucinated garbage to step 3.
