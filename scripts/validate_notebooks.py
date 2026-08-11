"""Validate every notebook and execute labs that passed the professional gate."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).parents[1]
PROFESSIONAL_MARKERS = (
    "## Scenario",
    "experimental question",
    "## Baseline",
    "Failure injection",
    "Diagnose the failure",
    "Production upgrade",
    "When not to use",
    "Exercises",
    "Advanced challenge",
    "OPENAI_API_KEY",
)


def notebook_paths() -> list[Path]:
    legacy = list((ROOT / "notebooks").glob("*.ipynb"))
    canonical = list((ROOT / "curriculum").glob("*/*/*.ipynb"))
    return sorted(legacy + canonical)


def validate(document, path: Path) -> bool:
    cell_ids = [cell.get("id") for cell in document.cells]
    if not all(cell_ids) or len(cell_ids) != len(set(cell_ids)):
        raise RuntimeError(f"{path} has missing or duplicate cell IDs")
    source = "\n".join("".join(cell.source) for cell in document.cells)
    metadata = document.metadata.get("prompt_course", {})
    professional = metadata.get("quality") == "professional-lab-v1"
    if professional:
        missing = [marker for marker in PROFESSIONAL_MARKERS if marker.lower() not in source.lower()]
        if missing:
            raise RuntimeError(f"{path} is marked professional but misses: {missing}")
        if not metadata.get("execute"):
            raise RuntimeError(f"{path} is professional but not enabled for execution")
    return professional


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute canonical notebooks marked professional-lab-v1.",
    )
    parser.add_argument(
        "--execute-everything",
        action="store_true",
        help="Execute every legacy and canonical notebook (maintainer migration check).",
    )
    args = parser.parse_args()

    paths = notebook_paths()
    completed = 0
    executed = 0
    for notebook in paths:
        document = nbformat.read(notebook, as_version=4)
        professional = validate(document, notebook)
        completed += int(professional)
        if args.execute_everything or (args.execute and professional):
            NotebookClient(document, timeout=180, kernel_name="python3").execute(cwd=ROOT)
            executed += 1
    print(
        f"Validated {len(paths)} notebooks; {completed} professional labs; "
        f"executed {executed}."
    )


if __name__ == "__main__":
    main()
