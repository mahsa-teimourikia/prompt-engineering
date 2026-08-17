"""Static checks for the GitHub Pages learning experience."""

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_every_course_topic_is_present_in_hub_and_quiz():
    lessons = (ROOT / "hub" / "lessons.js").read_text()
    lesson_ids = re.findall(r'"id":\s*"([^"]+)"', lessons)
    assert len(lesson_ids) == 29
    assert len(set(lesson_ids)) == 29
    assert "export const checks =" in lessons
    for level in ("beginner", "intermediate", "advanced", "enterprise"):
        assert (ROOT / "curriculum" / level).is_dir()


def test_quiz_and_hub_keep_their_deployed_relative_paths():
    quiz_page = (ROOT / "hub" / "quiz" / "index.html").read_text()
    hub_script = (ROOT / "hub" / "app.js").read_text()

    assert "Fifty-eight selectable questions" in quiz_page
    assert 'href="../"' in quiz_page
    assert 'href="quiz/"' in hub_script
    assert "Open reusable lab" not in hub_script
    assert "selected.lab" not in hub_script


def test_lesson_registry_is_valid_browser_module_syntax():
    source = (ROOT / "hub" / "lessons.js").read_text()
    result = subprocess.run(
        ["node", "--input-type=module", "--eval", source],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
