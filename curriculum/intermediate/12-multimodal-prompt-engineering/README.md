# 12 — Multimodal Prompt Engineering

## Learning objectives

Separate visual observation from inference, preserve page/region provenance,
handle OCR uncertainty and contradictory modalities, and return structured
extraction with a human-review path.

## Scenario and lab

Northstar reviews an invoice image and accompanying text. When visible and OCR
amounts disagree, the system must not guess. The
[notebook](multimodal_prompt_engineering.ipynb) uses an offline reconciliation
experiment; [lab.py](lab.py) exposes the uncertainty contract.

## Patterns, evaluation, and production

Use task-specific extraction schemas, page/region identifiers, modality labels,
and confidence fields. Measure field accuracy, provenance completeness,
contradiction detection, calibration, latency, and escalation quality. Test
blurred scans, tables, charts, screenshots, malicious documents, and text that
contradicts visual evidence. Treat OCR and image content as untrusted data;
validate business joins and authorization outside the model.

## References

- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
