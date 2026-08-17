# 11 — Tool Calling and Tool Interface Design

## Learning Objectives
- **Understand Tool Mechanics:** Learn that models do not "call" APIs; they generate JSON payloads that the application executes.
- **Design Tool Schemas:** Write clear, descriptive function signatures (tools) that the model can understand and select.
- **Implement Execution Loops:** Build the application code that catches the tool call, executes the Python function, and returns the result to the model.
- **Secure Tool Execution:** Recognize the extreme dangers of giving LLMs write-access to databases or execution environments.

## Core Concepts & Workflow

LLMs are trapped in a text box. They cannot query a live database, check the current weather, or send an email. Tool Calling (also known as Function Calling) provides an escape hatch.

You provide the model with a list of available tools, defined as JSON schemas (e.g., `get_weather(location: string)`). When the user asks "What's the weather in Tokyo?", the model realizes it needs external data. Instead of generating a text response, it generates a structured `ToolCall` payload. 

Crucially, the model *pauses*. It is the **Application's job** to catch that payload, actually execute the Python `get_weather` function, and append the `ToolResponse` back to the conversation history so the model can read it and generate a final human-readable answer.

![Tool Calling Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Trying to use regex to parse model text outputs like `Action: get_weather, Location: Tokyo`.

**Current State of the Art:**
1. **Native Function Calling:** Providers (like the **Google GenAI SDK** and OpenAI) have fine-tuned their models specifically for tool use. You pass Python functions directly to the SDK, and the API natively enforces the generation of exact JSON arguments.
2. **Parallel Tool Calling:** SOTA models can realize they need multiple pieces of information at once and emit several tool calls in a single generation step (e.g., calling `get_weather("Tokyo")` and `get_weather("Kyoto")` simultaneously).
3. **Agentic Frameworks:** Tools like **LangChain** and **Semantic Kernel** provide massive libraries of pre-built tools (web searchers, SQL executors, GitHub integrators) that can be immediately bound to an LLM.

## Lab and Production

### The Lab
The [notebook](11_tool_calling_and_tool_interface_design.ipynb) walks through the complete Tool Calling loop using the Google GenAI SDK. It defines a mock Python function, registers it as a tool with the model, simulates the model pausing to request the tool execution, and demonstrates the application returning the tool result for the final synthesis.

### Production Best Practices
- **Human-in-the-Loop for Writes:** Never give a model a tool that performs a destructive or irreversible action (like `drop_database` or `send_email`) without pausing the workflow to require explicit human approval (HITL).
- **Idempotency:** LLMs will frequently hallucinate arguments, retry failed calls, or get stuck in loops calling the same tool. Tool execution must be safe to run multiple times (idempotent).
- **Document the Schema:** The model relies on the `description` fields of your tool parameters. "get_user_id" is bad. "Looks up a user's ID based on their exact email address" is a good tool description.
