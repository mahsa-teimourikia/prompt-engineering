# 25 — Prompt Governance and Responsible AI

## Learning Objectives
- **Implement Data Redaction:** Automatically scrub PII, PHI, and PCI data from prompts before they leave your network.
- **Enforce Output Guardrails:** Block models from generating toxic, biased, or highly restricted content.
- **Understand Compliance Constraints:** Align prompt engineering practices with GDPR, HIPAA, and emerging AI regulations.
- **Audit Model Lineage:** Maintain a strict ledger of which models and prompts were used to make high-stakes decisions.

## Core Concepts & Workflow

As AI moves from internal tools to user-facing applications, Governance and Responsible AI become paramount. Sending a user's Social Security Number to a third-party LLM API is a catastrophic breach of compliance (e.g., HIPAA, GDPR, PCI). Similarly, allowing a customer-facing chatbot to generate toxic language or hallucinate legal advice creates massive liability.

Enterprise governance requires an impenetrable layer between the application and the LLM. This involves Inbound Guardrails (redacting sensitive data before it hits the API) and Outbound Guardrails (scanning the model's response for toxicity, bias, or restricted topics before showing it to the user).

![Governance Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Trusting the model provider's built-in "safety filters" to handle all compliance and toxicity requirements.

**Current State of the Art:**
1. **PII Redaction Engines:** Tools like **[Microsoft Presidio](https://microsoft.github.io/presidio/)** or **Google Cloud DLP** are used to scan outbound prompts, detect PII/PHI (like names, SSNs, medical data), and replace them with synthetic tokens (e.g., `[REDACTED_NAME]`) before the data is sent to the LLM.
2. **Enterprise Guardrails:** Frameworks like **[NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)** or **Lakera** enforce strict topic boundaries. If a user asks a banking bot about politics, the guardrail intercepts the request and blocks it before it ever reaches the expensive LLM.
3. **Data Residency and Sovereign Cloud:** SOTA governance often dictates that specific workloads cannot leave a geographic region. Prompt routing layers automatically ensure EU user requests are only routed to EU-hosted model endpoints.

## Lab and Production

### The Lab
The [notebook](25_prompt_governance_and_responsible_ai.ipynb) demonstrates building a strict interception proxy. It shows how to use Regex and basic NLP to detect simulated PII in a user prompt, redact it, send the clean prompt to the LLM, and then reconstruct the output. It also implements an outbound safety check to block toxic responses.

### Production Best Practices
- **Defense in Depth:** Do not rely solely on prompt instructions (e.g., "Do not reveal PII"). LLMs are easily jailbroken. Redaction must happen in deterministic code *before* the API call.
- **Anonymization vs. Pseudonymization:** Understand the difference. Anonymization permanently destroys the link to the identity. Pseudonymization replaces the identity with a token (e.g., `USER_42`) so the LLM can reason about relationships, and the application can swap the real name back in later.
- **Auditability:** For high-stakes decisions (e.g., loan approval summaries), you must log the exact prompt, the exact model version, and the safety checks that passed, retaining these records for regulatory audits.
