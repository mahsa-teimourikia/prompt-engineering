"""Coding-agent task-contract checks for Course 19."""
def assess(task):
    required={"problem","scope","tests","completion"}
    return {"complete":required<=set(task),"missing":sorted(required-set(task))}
