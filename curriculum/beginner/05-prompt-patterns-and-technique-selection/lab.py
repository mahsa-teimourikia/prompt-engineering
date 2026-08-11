"""Technique selection decision table for Course 05."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Technique:
    name: str
    maturity: str
    solves: str
    cost: str
    avoid_when: str

TECHNIQUES = (
    Technique("direct instruction", "FOUNDATIONAL", "unclear task", "low", "the task lacks evidence"),
    Technique("contrastive examples", "PRACTICAL", "label boundary", "medium", "a direct contract already passes"),
    Technique("schema constraint", "FOUNDATIONAL", "unreliable interface", "low", "free text is intentionally required"),
    Technique("retrieval context", "PRACTICAL", "missing current evidence", "medium", "the source is unauthorized"),
    Technique("tool calling", "PRACTICAL", "bounded external information", "medium", "a deterministic function is sufficient"),
    Technique("planner and verifier", "MODEL-DEPENDENT", "complex decomposition", "high", "a single bounded workflow works"),
)

FAILURES = {
    "unclear_task": "direct instruction",
    "label_boundary": "contrastive examples",
    "invalid_output": "schema constraint",
    "missing_evidence": "retrieval context",
    "live_fact": "tool calling",
    "complex_subtasks": "planner and verifier",
}

def select(failure):
    name = FAILURES[failure]
    return next(item for item in TECHNIQUES if item.name == name)

def evaluate(candidate, observed_failure):
    return {"candidate": candidate.name, "addresses_failure": candidate.name == FAILURES[observed_failure],
            "maturity": candidate.maturity, "cost": candidate.cost}
