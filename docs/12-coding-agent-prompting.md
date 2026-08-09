# Prompt engineering for coding agents: from request to specification

## Coding prompts are software-change contracts

“Build authentication” hides architectural, security, compatibility, test, and deployment decisions. A productive coding-agent prompt gives a goal, repository context, constraints, acceptance tests, and feedback loop. It asks the agent to inspect before it edits and to report unresolved risk rather than claiming success.

## Specification template

```text
Goal: Add OIDC login to the existing service.
Repository context: inspect the current auth module, configuration, tests, and deployment docs first.
Constraints: use existing PostgreSQL users; no secrets in source; preserve current session API.
Plan: name affected files and propose the smallest safe change before editing.
Acceptance: add tests for login, expired token, role denial, and secret scanning.
Verification: run the existing suite; report failures and residual risks.
```

## Control loop

`inspect → plan → implement → test → read failures → repair → summarize`. Keep a human approval gate before broad refactors, dependency upgrades, destructive migrations, or deployment changes. Provide only the relevant repository context and keep generated diffs/test output as evidence.

## Failure modes

| Failure | Better instruction/control |
| --- | --- |
| Agent rewrites unrelated code | constrain scope and require an affected-files plan. |
| Code compiles but violates product behavior | specify acceptance tests and run them. |
| Agent commits secrets or unsafe config | secret scanning, least privilege, and review gate outside prompt. |
| Endless repair loop | test/retry budget and escalation condition. |

## Guided exercise

Write a coding-agent contract for adding an audited `refund_request` endpoint without executing refunds. Include repository inspection, schema migration constraints, authorization rule, tests, and rollback plan. Then identify which requirements cannot be guaranteed by prompt text alone.

## References

- [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting)
- [OWASP Secure AI Model Ops](https://cheatsheetseries.owasp.org/cheatsheets/Secure_AI_Model_Ops_Cheat_Sheet.html)
