"""Offline tool-selection contract for Course 11."""
TOOLS={"get_order_status":{"required":{"order_id"},"read_only":True},"draft_refund":{"required":{"order_id","reason"},"read_only":True}}
def select(name,args):
    if name not in TOOLS:return False,"unknown tool"
    if not TOOLS[name]["required"]<=set(args):return False,"missing arguments"
    return True,"proposal valid; authorization still required"
