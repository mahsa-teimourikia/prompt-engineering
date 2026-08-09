from common import CaseBrief

INVOICE_OCR = {"invoice_id": "INV-104", "total": "42.00", "confidence": 0.91, "page": 1}
if __name__ == "__main__":
    case = CaseBrief(intent="refund", answer="Invoice INV-104 shows 42.00 on page 1; confirm the order id before a refund review.", evidence=["invoice:page-1"], needs_human=True)
    print(case.model_dump_json(indent=2)); assert INVOICE_OCR["confidence"] >= 0.9
