# 11 — Tool Calling and Tool Interface Design

## Learning objectives

Design narrow tool schemas, evaluate selection and arguments, interpret tool
results as untrusted data, and distinguish a model’s proposed call from
application authorization.

## Scenario and lab

Northstar can read order status or draft a refund request. It cannot execute a
refund.

![Tool Calling Lifecycle](./diagram-1.svg)

The [notebook](11_tool_calling_and_tool_interface_design.ipynb) demonstrates the full 
manual execution loop of a tool call: defining a tool, receiving a tool call request 
from the model, executing the tool locally, and returning the result to the model.

## Technology landscape and state of the art

**Foundational:** Tool Calling (or Function Calling) allows an LLM to request the execution of a deterministic function by outputting structured JSON arguments matching a predefined schema.

**Current State of the Art:**
1. **Pydantic Schemas:** Instead of writing raw JSON schemas to define tools, modern frameworks use Python type hints and Pydantic models. The SDK automatically translates these into the underlying JSON schema required by the API.
2. **Automatic vs. Manual Execution:** SDKs like `google-genai` can automatically execute Python functions if provided. However, for production systems (especially those involving destructive actions like `execute_refund`), developers often opt for the *manual* execution loop to maintain a strict security boundary and handle authorization.

## Patterns and production

Use precise names, descriptions, enums, required fields, and narrow scopes. Measure selection accuracy, argument accuracy, unnecessary calls, tool errors, and recovery. Validate every result, re-authorize at effect time, keep tools least-privilege and idempotent, and never treat a tool description as access control.

## References

- [OpenAI function calling guide](https://platform.openai.com/docs/guides/function-calling)
