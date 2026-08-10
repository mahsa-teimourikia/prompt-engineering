import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


parser = argparse.ArgumentParser(description="Validate or execute course notebooks.")
parser.add_argument("--execute", action="store_true", help="Execute notebooks after validating JSON.")
args = parser.parse_args()

for notebook in Path("notebooks").glob("*.ipynb"):
    document = nbformat.read(notebook, as_version=4)
    source = "\n".join("".join(cell.source) for cell in document.cells)
    if "labs/" in source:
        raise RuntimeError(f"{notebook} still depends on a separate lab.")
    if args.execute:
        NotebookClient(document, timeout=120, kernel_name="python3").execute(cwd=Path.cwd())
print("Notebook JSON validation passed.")
