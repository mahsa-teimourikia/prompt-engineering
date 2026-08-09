from common import build_case, retrieve

MAX_STEPS = 3
if __name__ == "__main__":
    state = {"question": "Can I get a refund?", "evidence": [], "steps": 0}
    while not state["evidence"] and state["steps"] < MAX_STEPS:
        state["evidence"] = retrieve("refund"); state["steps"] += 1
    output = build_case(state["question"], state["evidence"])
    print({"state": state, "output": output.model_dump()}); assert state["steps"] <= MAX_STEPS
