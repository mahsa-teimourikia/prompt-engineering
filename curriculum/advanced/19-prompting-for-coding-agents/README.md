# 19 — Prompting for Coding Agents

## Learning Objectives
- **Understand Agent Capabilities:** Recognize the shift from simple code completion to autonomous codebase engineering.
- **Define Engineering Contracts:** Learn how to write strict problem statements and scope restrictions for agents.
- **Implement Test-Driven Agents:** Require agents to generate passing unit tests to verify their work before reporting success.
- **Secure Agent Operations:** Isolate agent execution environments to prevent catastrophic system damage.

## Core Concepts & Workflow

We are moving past the era of sending a single snippet of code to an LLM and asking "why is this broken?" Autonomous Coding Agents can now operate across entire repositories, read thousands of files, propose architecture changes, and execute terminal commands to run builds or tests.

Because these agents are so powerful, a vague prompt like "fix authentication" is dangerous—it can lead to the agent rewriting massive, unrelated parts of the codebase. The state of the art involves defining strict "Task Contracts" that explicitly scope which files the agent is allowed to touch, what terminal commands it is authorized to run, and exactly which tests it must pass to prove the task is complete.

## Technology Landscape and State of the Art

**Foundational:** Sending a snippet of code to an LLM and asking "why is this broken?"

**Current State of the Art:** 
1. **Autonomous Coding Agents:** Tools like **GitHub Copilot Workspace**, **Devin**, and advanced IDEs like **[Cursor](https://www.cursor.com/)** or CLI agents like **[Aider](https://aider.chat/)** can now operate across an entire codebase. They can read thousands of files, propose architecture changes, and execute terminal commands.
2. **Engineering Contracts:** Because these agents are so powerful, a vague prompt like "fix authentication" is dangerous. It can lead to the agent rewriting massive, unrelated parts of the codebase. The state of the art involves defining strict "Task Contracts" that explicitly scope which files the agent is allowed to touch and which tests it must pass before reporting success.

## Lab and Production

### The Lab
The [notebook](19_prompting_for_coding_agents.ipynb) demonstrates the profound difference between a vague request and a structured engineering contract. It uses Pydantic to force the *human* to define a strict problem statement, file scope, and test criteria before handing the task off to an autonomous agent.

### Production Best Practices
- **Test-Driven Operations:** A coding agent must inspect the repository, propose a plan, make minimal changes, run tests, review the diff, and report evidence. It should not be allowed to submit a PR if the test suite fails.
- **Sandboxing:** Never give an agent unconstrained production access or unrestricted terminal access on your host machine. Always execute agent terminal commands in ephemeral Docker containers or secure sandboxes.
- **Human Review:** Agent PRs must go through standard human code review. The generated code must adhere to organizational style guides and security standards.
