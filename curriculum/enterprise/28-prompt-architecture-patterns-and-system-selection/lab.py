"""Least-complex architecture selector for Course 28."""
def choose(needs):
    if needs["deterministic"]: return "deterministic software"
    if needs["evidence"] and needs["action"]: return "tool-using workflow"
    if needs["evidence"]: return "retrieval-grounded generation"
    return "single prompt"
