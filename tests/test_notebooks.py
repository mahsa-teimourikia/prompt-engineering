import json
from pathlib import Path

ROOT = Path(__file__).parents[1]

def test_every_course_notebook_is_self_contained():
    notebooks = sorted((ROOT / "curriculum").glob("**/*.ipynb"))
    assert len(notebooks) >= 29
    for path in notebooks:
        with open(path, "r", encoding="utf-8") as f:
            document = json.load(f)
        cells = document.get("cells", [])
        assert len(cells) >= 1
        source = "\n".join("".join(cell.get("source", [])) for cell in cells)
        assert "labs/" not in source
