"""Behavior-artifact release gate for Course 22."""
ARTIFACT={"prompt":"v2","model":"adapter-A","context_policy":"selected","schema":"case-v1","eval":"suite-v3","limits":"500 tokens"}
def release(artifact, score): return bool(artifact.keys()>={"prompt","model","context_policy","schema","eval","limits"} and score>=.85)
