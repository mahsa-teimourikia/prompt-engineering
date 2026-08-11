"""Governance inventory completeness check for Course 25."""
REQUIRED={"id","owner","purpose","risk","model","sources","eval","status","last_review"}
def valid(record): return REQUIRED<=set(record)
