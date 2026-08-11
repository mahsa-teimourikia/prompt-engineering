"""Offline multimodal evidence reconciliation for Course 12."""
def extract(visible_amount,text_amount):
    if visible_amount != text_amount:
        return {"amount":None,"confidence":"low","needs_human":True,"reason":"visual and text evidence conflict"}
    return {"amount":visible_amount,"confidence":"high","needs_human":False,"reason":"sources agree"}
