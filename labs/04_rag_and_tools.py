from common import build_case, retrieve

TOOLS = {"get_refund_policy": lambda: retrieve("refund")}
if __name__ == "__main__":
    evidence = TOOLS["get_refund_policy"]()
    result = build_case("Can I get a refund?", evidence)
    print({"tool": "get_refund_policy", "result": result.model_dump()}); assert result.evidence
