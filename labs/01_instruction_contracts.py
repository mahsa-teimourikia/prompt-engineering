from common import build_case, retrieve

CONTRACT = """Classify the request. Use supplied policy only. State uncertainty. Do not execute actions. Return intent, answer, evidence, and escalation."""

if __name__ == "__main__":
    case = build_case("Can I get a refund for order 55?", retrieve("refund"))
    print(CONTRACT); print(case.model_dump_json(indent=2)); assert case.intent == "refund"
