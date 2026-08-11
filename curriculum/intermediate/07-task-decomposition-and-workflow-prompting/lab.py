"""Offline workflow comparison for Course 07."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Document:
    text: str
    policy: str

def one_prompt(document):
    return {"decision": "approve", "trace": ("single call",), "supported": False, "stages": 1}

def workflow(document):
    extracted = {"order_id": "42" if "42" in document.text else None, "request": "refund"}
    evidence = document.policy if extracted["order_id"] else None
    decision = "draft_for_review" if evidence else "clarify"
    return {"decision": decision, "trace": ("extract", "check evidence", "draft"), "supported": bool(evidence), "stages": 3}

def score(result):
    return {"supported": result["supported"], "stages": result["stages"], "debuggable": len(result["trace"]) > 1}

DOCUMENT = Document("Customer requests a refund for order 42.", "refunds require order review")
