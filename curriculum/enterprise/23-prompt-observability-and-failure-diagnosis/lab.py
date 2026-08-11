"""Trace-based regression diagnosis for Course 23."""
TRACES=({"version":"v1","model":"A","context":"fresh","valid":True},{"version":"v2","model":"A","context":"stale","valid":False})
def diagnose(trace): return "stale context" if trace["context"]=="stale" else "no regression"
