# 13 — Prompt Security and Untrusted Content

## Learning objectives

Model direct and indirect prompt injection, isolate untrusted content, apply
deterministic authorization and output controls, and retest attacks rather than
assuming a longer system prompt is a security boundary.

## Attack-and-defense workflow

    vulnerable design → attack → trace failure → prompt/context mitigation
    → application control → retest

Northstar receives a malicious retrieved document asking it to approve a refund
and exfiltrate data. The model may classify or draft; only deterministic code
can authorize an effect or data release.

## Lab, evaluation, and production

The [notebook](prompt_security_and_untrusted_content.ipynb) compares a
vulnerable implementation with a defended path. [lab.py](lab.py) makes the
security outcome observable. Test direct/indirect injection, tool-output
poisoning, cross-tenant data, jailbreaks, and data-exfiltration attempts.
Measure attack success, control coverage, false positives, safe escalation, and
time to detect. Use least-privilege tools, tenant isolation, approvals,
allow-lists, result validation, audit logs, and incident response.

## References

- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
