"""Offline conversation-context strategies for Course 09."""
HISTORY=("User prefers email updates.","Order 42 is delayed.","Unrelated product discussion.","Please summarize my order status.")
def context(strategy):
    if strategy=="full": selected=HISTORY
    elif strategy=="window": selected=HISTORY[-2:]
    elif strategy=="summary": selected=("preference=email; order=42 delayed",HISTORY[-1])
    elif strategy=="retrieval": selected=(HISTORY[0],HISTORY[1],HISTORY[-1])
    else: raise ValueError(strategy)
    return {"strategy":strategy,"selected":selected,"tokens":sum(len(x.split()) for x in selected),
            "retains_order":any("42" in x for x in selected),"retains_preference":any("email" in x for x in selected)}
