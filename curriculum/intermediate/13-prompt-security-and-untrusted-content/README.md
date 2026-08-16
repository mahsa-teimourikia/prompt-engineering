# 13 — Prompt Security and Untrusted Content

## Learning objectives

Model direct and indirect prompt injection, isolate untrusted content, apply
deterministic authorization and output controls, and retest attacks rather than
assuming a longer system prompt is a security boundary.

## Attack-and-defense workflow

![Attack-and-Defense Workflow](./diagram-1.svg)

Northstar receives a malicious retrieved document asking it to approve a refund
and exfiltrate data. The model may classify or draft; only deterministic code
can authorize an effect or data release.

## Technology landscape and state of the art

**Foundational:** LLMs take in text and output text. Fundamentally, they lack a dedicated "instruction channel" separate from the "data channel". Everything is just tokens.
**Current State of the Art:**
1. **The Inevitability of Injection:** Security research currently treats Prompt Injection as an unsolved, and potentially unsolvable, problem at the model layer. If a model is smart enough to follow your instructions, it is smart enough to follow the user's instructions hidden in the data.
2. **Defense in Depth:** Modern systems rely on Defense in Depth. They use XML tagging (`<untrusted_data>`) to help the model distinguish context, but they never rely on the model for security. The ultimate boundary is **Application Control**—the model can draft a refund, but only a human or rigid deterministic code can execute it.

## Lab, evaluation, and production

The [notebook](13_prompt_security_and_untrusted_content.ipynb) demonstrates Indirect Prompt Injection and compares a vulnerable implementation with a defended path. Test direct/indirect injection, tool-output poisoning, cross-tenant data, jailbreaks, and data-exfiltration attempts. Measure attack success, control coverage, false positives, safe escalation, and time to detect. Use least-privilege tools, tenant isolation, approvals, allow-lists, result validation, audit logs, and incident response.

## References

- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
