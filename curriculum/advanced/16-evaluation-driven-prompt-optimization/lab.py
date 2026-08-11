"""One-variable optimization loop for Course 16."""
RUNS=(("baseline",.50,.80),("add_boundary_example",.75,.78),("change_schema",.70,.92))
def accept(run): return run[1]>.50 and run[2]>=.80
