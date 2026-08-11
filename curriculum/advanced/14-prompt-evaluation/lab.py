"""Deterministic prompt experiment harness for Course 14."""
CASES=(("clear","refund","refund"),("ambiguous","unknown","refund"),("missing","unknown","unknown"))
def evaluate(candidate):
    rows=[]
    for name,expected,baseline in CASES:
        observed=expected if candidate=="safe" else baseline
        rows.append({"slice":name,"expected":expected,"observed":observed,"correct":expected==observed})
    return rows
def metrics(rows): return {"accuracy":sum(x["correct"] for x in rows)/len(rows),"failures":[x["slice"] for x in rows if not x["correct"]]}
