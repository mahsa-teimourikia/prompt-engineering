"""Offline schema validation for Course 04."""
import json

SAMPLES = {
    "valid": '{"intent":"refund","answer":"Share the order ID.","evidence_id":"refund-v3","needs_human":false}',
    "malformed": '{"intent":"refund"',
    "enum": '{"intent":"payment","answer":"Review it.","evidence_id":"refund-v3","needs_human":false}',
    "extra": '{"intent":"refund","answer":"Review it.","evidence_id":"refund-v3","needs_human":false,"priority":"high"}',
    "semantic": '{"intent":"refund","answer":"You are eligible for a refund.","evidence_id":"refund-v3","needs_human":false}',
}

def validate(raw):
    try: value = json.loads(raw)
    except json.JSONDecodeError: return False, "invalid JSON"
    if set(value) != {"intent","answer","evidence_id","needs_human"}: return False, "schema fields do not match"
    if value["intent"] not in {"refund","shipping","account"}: return False, "enum violation"
    if not isinstance(value["needs_human"], bool): return False, "wrong boolean type"
    if not value["evidence_id"] or "eligible" in value["answer"].lower(): return False, "semantic/evidence violation"
    return True, "valid"

def bounded_repair(raw):
    try: value = json.loads(raw)
    except json.JSONDecodeError: return None
    value = {k:v for k,v in value.items() if k in {"intent","answer","evidence_id","needs_human"}}
    return json.dumps(value) if value.get("intent") in {"refund","shipping","account"} else None
