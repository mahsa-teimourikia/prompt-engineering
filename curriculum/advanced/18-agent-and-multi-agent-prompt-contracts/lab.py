"""Offline agent-trajectory comparison for Course 18."""
def workflow(): return {"steps":("classify","retrieve","draft"),"tools":1,"stopped":True,"success":True}
def supervisor(): return {"steps":("supervisor","researcher","reviewer","handoff"),"tools":2,"stopped":True,"success":True}
def evaluate(x): return {"success":x["success"],"tool_calls":x["tools"],"bounded":x["stopped"],"trajectory":x["steps"]}
