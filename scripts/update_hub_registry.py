"""Keep Hub claims and artifact links aligned with the curriculum."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "hub" / "lessons.js"


COPY = {
    "behavior": ("Test how prompt position, sampling, and missing evidence affect behavior.", "Compare controlled variants and require explicit abstention when evidence is absent."),
    "contracts": ("Turn an ambiguous request into a testable behavior contract.", "Specify inputs, authority, constraints, output, and failure states, then validate them in code."),
    "examples": ("Select examples that clarify real decision boundaries.", "Compare zero-shot, static, random, and similarity-based examples without hiding context cost."),
    "structured": ("Treat model output as an untrusted proposal for a typed interface.", "Separate syntax constraints from semantic and business validation, including bounded repair."),
    "patterns": ("Choose a technique from an observed failure rather than a trend.", "Compare techniques on quality and context cost, then keep the smallest useful intervention."),
    "reasoning": ("Choose the smallest reasoning architecture that improves a verified decision.", "Compare direct, sampled, and verifier-assisted approaches without exposing private chain-of-thought."),
    "workflow": ("Decompose complex work into observable, recoverable stages.", "Use typed handoffs, stop conditions, and failure-aware workflow state."),
    "context": ("Build a context contract with authority, scope, provenance, and budget.", "Select, order, and validate context while treating retrieved content as untrusted data."),
    "conversation": ("Separate message history, application state, and durable memory.", "Compare window, summary, and structured-state strategies with retention and tenant boundaries."),
    "rag": ("Design an evidence interface that can cite, abstain, and surface conflicts.", "Evaluate retrieval and answer support separately while authorizing before retrieval."),
    "tools": ("Give models narrow typed capabilities while the application owns execution.", "Validate arguments, authorize before exposure, and distinguish proposed calls from completed actions."),
    "multimodal": ("Ground document and image claims in explicit regions and evidence IDs.", "Evaluate extraction, contradiction, and missing-evidence cases with a reproducible synthetic asset."),
    "security": ("Model prompt injection as a trust-boundary failure, not a wording puzzle.", "Combine untrusted-data separation with least privilege, authorization, validation, and adversarial tests."),
    "evaluation": ("Replace anecdotal checks with versioned cases, slices, and hard gates.", "Compare baseline and candidate metrics while retaining denominators and critical failures."),
    "judges": ("Calibrate rubric judges against human labels and known bias tests.", "Measure agreement, handle ties and order effects, and route ambiguous or high-impact cases to people."),
    "optimization": ("Improve measured behavior without leaking the final test set.", "Separate development and holdout data and reject local fixes that cause global regressions."),
    "dspy": ("Search a bounded prompt-program space against an explicit metric.", "Select on development data, test once on holdout, and inspect leakage and metric gaming."),
    "agents": ("Design bounded agent tasks with typed contracts, budgets, and terminal states.", "Authorize from trusted identity before capability exposure and justify multi-agent complexity against a baseline."),
    "coding": ("Turn a software request into an enforceable change contract.", "Constrain file and command scope, then require tests and diff evidence before completion."),
    "models": ("Keep durable behavior contracts separate from provider adapters.", "Compare conformance, quality, latency, and cost before selecting or migrating a model."),
    "efficiency": ("Optimize cost and latency without dropping required evidence.", "Trace quality and resource use together and reject configurations that are merely cheaper failures."),
    "promptops": ("Version and release the complete AI behavior artifact.", "Gate prompt, schema, model configuration, dataset, and ownership changes with reproducible evidence."),
    "observability": ("Capture privacy-aware traces that identify the first failing layer.", "Record correlation, versions, evidence, policy, usage, errors, and terminal state without hidden reasoning."),
    "release": ("Run sticky canaries with declared metrics and rollback rules.", "Distinguish insufficient samples from success and roll back immediately on critical failures."),
    "governance": ("Connect AI policy to executable controls, evidence, ownership, and approval.", "Use trusted, versioned approval records and fail closed when required evidence is missing."),
    "trust": ("Calibrate user trust with evidence, impact-aware review, and honest uncertainty.", "Route by risk and support rather than treating model confidence as permission."),
    "portability": ("Test provider adapters against one contract and shared cases.", "Normalize results and allow fallback only when operation semantics make retry safe."),
    "architecture": ("Select the least complex architecture that meets explicit constraints.", "Expose weighted criteria, compare alternatives, and test recommendation sensitivity."),
    "capstone": ("Assemble a release portfolio for the complete Northstar system.", "Pass a fail-closed gate covering contract, evaluation, threat, trace, ownership, tests, and rollback."),
}


def replace_field(source: str, lesson_id: str, field: str, value: str) -> str:
    pattern = rf'("id":\s*"{re.escape(lesson_id)}".*?"{field}":\s*)"[^"]*"'
    replacement = lambda match: match.group(1) + '"' + value.replace('"', '\\"') + '"'
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"could not update {field} for {lesson_id}")
    return updated


def main() -> None:
    source = PATH.read_text(encoding="utf-8")
    for lesson_id, (summary, outcome) in COPY.items():
        source = replace_field(source, lesson_id, "summary", summary)
        source = replace_field(source, lesson_id, "outcome", outcome)

    source = re.sub(r'^\s+"(?:lab|checkpoint)":\s*"[^"]+",?\n', "", source, flags=re.M)

    def add_artifacts(match: re.Match[str]) -> str:
        indentation, notebook_value = match.groups()
        notebook = Path(notebook_value)
        number = int(notebook.parent.name[:2])
        lab = notebook.parent / f"lab{number:02d}.py"
        checkpoint = notebook.parent / "README.md"
        return (
            f'{indentation}"notebook": "{notebook_value}",\n'
            f'{indentation}"lab": "{lab.as_posix()}",\n'
            f'{indentation}"checkpoint": "{checkpoint.as_posix()}#checkpoint",'
        )

    source, count = re.subn(
        r'^(\s+)"notebook":\s*"(curriculum/[^"]+\.ipynb)",?',
        add_artifacts,
        source,
        flags=re.M,
    )
    if count != 28:
        raise RuntimeError(f"expected 28 single-notebook entries, found {count}")
    capstone_marker = '    ],\n    "refs": []\n  }\n];'
    capstone_artifacts = (
        '    ],\n'
        '    "lab": "curriculum/enterprise/29-ai-system-engineering-capstone/lab29.py",\n'
        '    "checkpoint": "curriculum/enterprise/29-ai-system-engineering-capstone/README.md#checkpoint",\n'
        '    "refs": []\n  }\n];'
    )
    if capstone_marker not in source:
        raise RuntimeError("could not locate capstone artifact list")
    source = source.replace(capstone_marker, capstone_artifacts, 1)
    PATH.write_text(source, encoding="utf-8")


if __name__ == "__main__":
    main()
