from pathlib import Path

import nbformat


ROOT = Path(__file__).parents[1]


def test_every_course_notebook_is_self_contained():
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    assert len(notebooks) == 9
    for path in notebooks:
        document = nbformat.read(path, as_version=4)
        source = "\n".join("".join(cell.source) for cell in document.cells)
        assert "labs/" not in source
        assert "Shared deterministic Northstar fixtures" in source


def test_no_separate_lab_source_files_remain():
    lab_directory = ROOT / "labs"
    assert not lab_directory.exists() or not list(lab_directory.glob("*.py"))
