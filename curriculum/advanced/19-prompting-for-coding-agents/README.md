# 19 — Prompting for Coding Agents

## Learning objectives

Write a repository-aware task contract, constrain file scope, specify tests and
completion evidence, and compare a vague request with a reviewable engineering
task.

## Lab and production

The [notebook](prompting_for_coding_agents.ipynb) checks a vague “fix
authentication” request against a structured contract. [lab.py](lab.py)
requires problem, scope, tests, and completion criteria. A coding agent must
inspect the repository, propose a plan, make minimal changes, run tests, review
the diff, and report evidence. Never give production access by prompt alone.

## References

- [GitHub repository custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
