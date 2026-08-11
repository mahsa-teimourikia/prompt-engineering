"""Static checks for the GitHub Pages learning experience."""

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_every_course_topic_is_present_in_hub_and_quiz():
    lessons = (ROOT / "hub" / "lessons.js").read_text()
    lesson_ids = re.findall(r'lesson\("([^"]+)"', lessons)
    checkpoint_ids = re.findall(r'^  "?([a-z][a-z-]*)"?: check\(', lessons, re.MULTILINE)
    documents = re.findall(r'"(\d\d-[^"]+\.md|curriculum/[^"]+/README\.md)"', lessons)
    notebooks = re.findall(r'"(\d\d_[^"]+\.ipynb|curriculum/[^"]+\.ipynb)"', lessons)

    assert len(lesson_ids) == 21
    assert len(set(lesson_ids)) == 21
    assert sorted(checkpoint_ids) == sorted(lesson_ids)
    assert len(documents) == len(notebooks) == 21
    assert all((ROOT / document if document.startswith("curriculum/") else ROOT / "docs" / document).is_file() for document in documents)
    assert all((ROOT / notebook if notebook.startswith("curriculum/") else ROOT / "notebooks" / notebook).is_file() for notebook in notebooks)


def test_quiz_and_hub_keep_their_deployed_relative_paths():
    quiz_page = (ROOT / "hub" / "quiz" / "index.html").read_text()
    hub_script = (ROOT / "hub" / "app.js").read_text()

    assert "Twenty-one selectable questions" in quiz_page
    assert 'href="../"' in quiz_page
    assert 'href="quiz/"' in hub_script


def test_lesson_registry_is_valid_browser_module_syntax():
    source = (ROOT / "hub" / "lessons.js").read_text()
    result = subprocess.run(
        ["node", "--input-type=module", "--eval", source],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
