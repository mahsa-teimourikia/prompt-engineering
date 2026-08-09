from common import UNTRUSTED_RUNBOOK, is_injection

if __name__ == "__main__":
    blocked = is_injection(UNTRUSTED_RUNBOOK)
    print({"content_is_data": True, "injection_detected": blocked, "action": "escalate"})
    assert blocked
