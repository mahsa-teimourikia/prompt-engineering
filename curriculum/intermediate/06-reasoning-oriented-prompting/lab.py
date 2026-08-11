"""Observable decomposition and verification experiment for Course 06."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Incident:
    symptoms: tuple[str, ...]
    evidence: tuple[str, ...]

def direct_answer(incident):
    return {"recommendation": "restart the service", "supported": False, "calls": 1}

def plan_and_verify(incident):
    plan = ("classify symptom", "check evidence", "recommend least-risk action")
    supported = "database connection errors" in incident.evidence
    return {"plan": plan, "assumption": "database outage is possible",
            "recommendation": "escalate database incident" if supported else "collect database trace",
            "verification": supported, "supported": True, "calls": 2}

INCIDENT = Incident(("checkout failures", "timeouts"), ("database connection errors",))

def score(result):
    return {"supported": result["supported"], "calls": result["calls"],
            "safe": result["recommendation"] != "restart the service"}
