"""Load the synthetic fixtures shipped with Northstar."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load(name: str) -> list[dict[str, Any]]:
    """Load a top-level fixture by filename stem."""

    path = FIXTURE_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))
