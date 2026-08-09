# Multimodal document prompting

## Visual input is evidence, not a shortcut to certainty

Modern models can reason across text, images, tables, screenshots, audio, and video. The core prompt-engineering principles do not change: define the task, provide only authorized context, distinguish observation from inference, request a consumable output, and provide a safe failure path.

Northstar receives an invoice screenshot with a disputed total. A credible assistant extracts what is visibly present, identifies uncertainty, cites the page or region, and prepares a review. It does not invent an unreadable amount or initiate a financial adjustment.

## Learning outcomes

- Design a visual-evidence contract for a document task.
- Separate OCR text, visible layout, and inferred business meaning.
- Request page/region provenance and uncertainty explicitly.
- Validate extracted fields before using them in a workflow.

## A multimodal evidence contract

```text
Objective: Extract invoice ID, line items, total, and page/region references.
Evidence rule: Report only values visible in the supplied document.
Uncertainty rule: Mark unreadable or conflicting fields as unknown; do not guess.
Output: typed extraction plus source page, confidence, and review flag.
Action rule: Never issue a credit, refund, or payment change.
```

| Layer | Example | Risk if confused |
| --- | --- | --- |
| Observation | “INV-104 is visible in header.” | Low, if location is cited. |
| OCR extraction | `total: 42.00` | OCR may misread decimal or character. |
| Inference | “Customer is eligible for refund.” | Requires policy and authorized order state, not image alone. |

## Worked example: invoice dispute

**Customer:** “This invoice charged me twice.”

**Visible document:** invoice number, two line items, total, and page one. It does not show the payment ledger.

**Correct output:** extract visible fields, cite `invoice:page-1`, state that duplicate charging cannot be verified from the invoice alone, and request payment-transaction evidence or specialist review. The visual model helps organize evidence; it must not transform a document into an unsupported financial conclusion.

## Step-by-step workflow

```text
Receive authorized file → validate file/type/tenant → extract visual facts
   → attach page/region provenance → validate schema/ranges
   → combine only with permitted records → draft response or escalate
```

Tables need special attention: row/column positions convey meaning. Preserve headers, units, page number, and footnotes. For screenshots, ask the model to identify the visible control or error code before explaining a possible cause. For audio, retain timestamps and never assume a transcript is complete.

## Guided practice

1. Run [the multimodal notebook](../notebooks/05_multimodal_prompting.ipynb).
2. Change OCR confidence from `0.91` to `0.55`; require a review flag.
3. Add a second page whose total conflicts with page one. Define the escalation response.
4. Write a schema with `source_page`, `source_region`, `confidence`, and `needs_human`.

## Failure modes

| Failure | Repair |
| --- | --- |
| Model invents a value from a blurred image | Require explicit unknown/low-confidence output and human review. |
| Table values lose row/column meaning | Preserve layout, headers, units, and source region. |
| Sensitive document is sent to an unauthorized model/provider | Apply data classification, retention, and tenant policy before invocation. |
| Extracted amount triggers automatic action | Validate against source systems and require approval for consequences. |
| Visual citation is absent | Include page/region identifiers in the structured output. |

## Before moving on

- Is every extracted fact traceable to a page, timestamp, or region?
- Does the contract distinguish visible observation from business inference?
- Are low-confidence fields and conflicts safe to route?
- Are file access, retention, and actions governed outside the prompt?

## References

- [Google prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [OpenAI image inputs](https://platform.openai.com/docs/guides/images-vision)
