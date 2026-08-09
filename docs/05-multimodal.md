# Multimodal document prompting

Images, tables, PDFs, and screenshots need the same contract discipline as text. Identify the task, define what visual evidence counts, request location-aware citations, and ask the model to distinguish visible facts from inferences. OCR text can be incomplete; a table's visual layout can change meaning.

For an invoice dispute, the model should extract invoice number, line items, and totals; flag unreadable fields; and cite page/region rather than infer a missing value. Validate all values before a financial workflow acts.

**References:** [Google multimodal prompting](https://ai.google.dev/gemini-api/docs/prompting-strategies), [OpenAI image inputs](https://platform.openai.com/docs/guides/images-vision).
