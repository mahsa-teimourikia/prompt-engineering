from pathlib import Path
import nbformat

for notebook in Path("notebooks").glob("*.ipynb"):
    nbformat.read(notebook, as_version=4)
print("Notebook JSON validation passed.")
