"""Structural checks for the numbered curriculum and Hub registry."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).parents[1]
LEVEL_RANGES = {
    "beginner": range(1, 6),
    "intermediate": range(6, 14),
    "advanced": range(14, 22),
    "enterprise": range(22, 30),
}
MATERIAL = re.compile(r'"material":\s*"([^"]+)"')
REGISTRY_PATH = re.compile(r'"(?:notebook|path)":\s*"([^"]+)"')


def course_directories() -> list[Path]:
    return sorted(
        path
        for level in LEVEL_RANGES
        for path in (ROOT / "curriculum" / level).iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name)
    )


def test_every_course_has_readme_notebook_and_diagram():
    courses = course_directories()
    assert len(courses) == 29
    for course in courses:
        number = course.name[:2]
        assert (course / "README.md").is_file(), course
        notebooks = sorted(course.glob(f"{number}_*.ipynb"))
        assert len(notebooks) == 1, course
        assert (course / "diagram-1.svg").is_file(), course


def test_course_numbering_is_contiguous_by_level():
    for level, expected in LEVEL_RANGES.items():
        numbers = sorted(int(path.name[:2]) for path in (ROOT / "curriculum" / level).iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))
        assert numbers == list(expected), level


def test_hub_registry_matches_curriculum_paths():
    source = (ROOT / "hub" / "lessons.js").read_text(encoding="utf-8")
    materials = MATERIAL.findall(source)
    assert len(materials) == 29
    assert {Path(path).parent for path in materials} == {
        path.relative_to(ROOT) for path in course_directories()
    }

    registry_paths = [
        path
        for path in REGISTRY_PATH.findall(source)
        if path.startswith("curriculum/")
    ]
    assert registry_paths
    assert all((ROOT / path).is_file() for path in registry_paths)


def test_no_notebook_has_committed_outputs():
    for path in ROOT.glob("curriculum/**/*.ipynb"):
        document = json.loads(path.read_text(encoding="utf-8"))
        for cell in document.get("cells", []):
            if cell.get("cell_type") == "code":
                assert not cell.get("outputs"), path
                assert cell.get("execution_count") is None, path
