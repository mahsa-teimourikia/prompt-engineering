"""Provider-neutral adapter comparison for Course 20."""
def run(model):
    return {"model":model,"contract_valid":True,"latency_ms":120 if model=="A" else 80,"cost":.02 if model=="A" else .01}
