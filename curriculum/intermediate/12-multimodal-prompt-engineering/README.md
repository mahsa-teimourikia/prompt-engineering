# 12 — Multimodal Prompt Engineering

## Learning objectives

Separate visual observation from inference, preserve page/region provenance,
handle OCR uncertainty and contradictory modalities, and return structured
extraction with a human-review path.

## Scenario and lab

Northstar reviews an invoice image and accompanying text. When visible and OCR
amounts disagree, the system must not guess.

![Multimodal Contradiction Workflow](./diagram-1.svg)

The [notebook](12_multimodal_prompt_engineering.ipynb) demonstrates how to handle
contradictory multimodal inputs by forcing the model to explicitly evaluate the
evidence and output an `is_contradictory` flag using a Pydantic schema, rather
than blindly trusting the user's text or hallucinating a compromise.

## Technology landscape and state of the art

**Foundational:** Integrating multiple streams of data (text, image, audio, video) into a single inference pass.

**Current State of the Art:**
1. **Native Multimodality:** Historically, dealing with images required a brittle pipeline: run an Optical Character Recognition (OCR) model to extract text from the image, and then feed that text to an LLM. Modern models like Gemini 1.5 are *natively* multimodal—they process the pixels directly alongside the text tokens, preserving spatial relationships and context that OCR destroys.
2. **Structured Uncertainty:** Because multimodal inputs often contain noise (e.g., blurry scans) or contradictions (e.g., user text claims $800, but the image shows $500), state-of-the-art systems use Structured Outputs (Pydantic) to force the model to declare its confidence or flag contradictions, allowing the application to safely route exceptions to humans.

## Patterns, evaluation, and production

Use task-specific extraction schemas, page/region identifiers, modality labels, and confidence fields. Measure field accuracy, provenance completeness, contradiction detection, calibration, latency, and escalation quality. Test blurred scans, tables, charts, screenshots, malicious documents, and text that contradicts visual evidence. Treat OCR and image content as untrusted data; validate business joins and authorization outside the model.

## References

- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
