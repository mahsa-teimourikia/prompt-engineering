from common import Trace

PROMPTS = {"v1": "Answer helpfully.", "v2": "Use approved policy only; cite evidence; abstain when unsupported."}
if __name__ == "__main__":
    baseline = Trace("v1", True, False, 90, 0.0008)
    candidate = Trace("v2", True, True, 110, 0.0011)
    release = candidate.valid and candidate.supported and candidate.estimated_cost <= 0.002
    print({"candidate": candidate, "release_gate": release, "rollback": "v1"}); assert release
