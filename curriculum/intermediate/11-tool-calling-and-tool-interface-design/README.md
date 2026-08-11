# 11 — Tool Calling and Tool Interface Design

## Learning objectives

Design narrow tool schemas, evaluate selection and arguments, interpret tool
results as untrusted data, and distinguish a model’s proposed call from
application authorization.

## Scenario and lab

Northstar can read order status or draft a refund request. It cannot execute a
refund. The [notebook](tool_calling_and_tool_interface_design.ipynb) tests an
unknown tool, missing parameters, and a valid proposal. [lab.py](lab.py) makes
the contract explicit.

## Patterns and production

Use precise names, descriptions, enums, required fields, and narrow scopes.
Measure selection accuracy, argument accuracy, unnecessary calls, tool errors,
and recovery. Validate every result, re-authorize at effect time, keep tools
least-privilege and idempotent, and never treat a tool description as access
control.

## References

- [OpenAI function calling guide](https://platform.openai.com/docs/guides/function-calling)
