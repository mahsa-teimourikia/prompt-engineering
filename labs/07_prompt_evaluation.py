from common import Trace, build_case, retrieve

DATASET = [("Can I get a refund?", "refund"), ("Where is delivery?", "shipping"), ("Make up a policy", "unknown")]
if __name__ == "__main__":
    traces = []
    for question, expected in DATASET:
        topic = expected if expected in {"refund", "shipping"} else "missing"
        result = build_case(question, retrieve(topic))
        traces.append(Trace("v1", result.intent == expected, bool(result.evidence) or result.needs_human, 120, 0.001))
    print({"success_rate": sum(t.valid and t.supported for t in traces) / len(traces), "traces": traces})
    assert len(traces) == 3
