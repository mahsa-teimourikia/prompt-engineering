# 26 — Human-Centred AI and Trust Calibration

## Learning objectives

Design useful uncertainty, abstention, explanation, escalation, and human
review; evaluate user-facing reliability rather than model confidence alone.

![Trust Calibration Flow](./diagram-1.svg)

## Technology landscape and state of the art

**Foundational:** Building chat interfaces that answer every question confidently, leading to "Automation Bias" where users blindly trust the AI even when it hallucinates.
**Current State of the Art:** 
1. **Calibrated Trust:** Enterprise AI systems are now designed to intentionally calibrate the user's trust. If the model is highly confident, it answers directly. If it is moderately confident, it surfaces citations or explicitly admits uncertainty (e.g., "I found this in the docs, but I am not certain").
2. **Human-in-the-Loop (HITL) Escalation:** Models are prompted to self-evaluate. If the query is ambiguous, dangerous, or outside their knowledge base, they output a structured escalation flag, handing the ticket over to a human Zendesk/ServiceNow agent rather than guessing.
3. **UX for Uncertainty:** The UI itself is changing. Instead of definitive text blocks, uncertain responses are rendered with visual cues (e.g., italics, different background colors, or explicit "Draft" watermarks) to signal to the user that human review is required.

## Lab and production

The [notebook](26_human_centred_ai_and_trust_calibration.ipynb) contrasts two AI support agents. The first is an "Overconfident Agent" that happily hallucinates an answer to a complex, ambiguous user query. The second is a "Calibrated Agent" that uses Pydantic structured outputs to evaluate its own confidence. When faced with the same ambiguous query, the Calibrated Agent outputs an `escalate_to_human: true` flag, allowing the system to route the ticket to a human rather than providing bad advice. Production systems define risk tiers, review queues, user controls, accessible explanations, recovery paths, and measures for automation bias.

## References

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
