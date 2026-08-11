"""Capstone readiness gate for Course 29."""
REQUIRED={"outcome","contract","schema","context","tools","security","eval","observability","release","rollback","adr"}
def ready(system): return REQUIRED<=set(system)
