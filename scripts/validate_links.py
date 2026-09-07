"""Validate relative Markdown, Hub registry, and quiz paths."""

from __future__ import annotations

from pathlib import Path
import re


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")
REGISTRY_PATH = re.compile(r'"(?:material|notebook|path)":\s*"([^"]+)"')
EXCLUDED = {".git", ".venv", "node_modules", "out"}


def _is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "tel:", "data:"))


def validate_links(root: Path) -> list[str]:
    broken: list[str] = []
    for path in root.rglob("*.md"):
        if any(part in EXCLUDED for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for link in MARKDOWN_LINK.findall(text):
            if _is_external(link):
                continue
            target = link.split("#", 1)[0] or "."
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{path.relative_to(root)} -> {link}")

    registry = root / "hub" / "lessons.js"
    if registry.exists():
        for target in REGISTRY_PATH.findall(registry.read_text(encoding="utf-8")):
            if _is_external(target):
                continue
            target = target.split("#", 1)[0]
            if not (root / target).exists():
                broken.append(f"hub/lessons.js -> {target}")

    return broken


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    broken = validate_links(root)
    if broken:
        print("Broken links:")
        print("\n".join(f"- {item}" for item in broken))
        return 1
    print("All relative Markdown, Hub, and quiz paths resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
