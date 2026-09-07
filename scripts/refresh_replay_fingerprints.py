"""Refresh demo replay fingerprints from the real PromptRequest implementation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from northstar.demo import DEMO_CASES, SupportClassification
from northstar.runtime import Message, PromptRequest


def main() -> None:
    path = ROOT / "northstar" / "fixtures" / "replays" / "demo.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    for case_id, text, _expected in DEMO_CASES:
        request = PromptRequest(
            case_id=case_id,
            system="Classify the ticket into one supported category.",
            messages=[Message(role="user", text=text)],
            response_schema=SupportClassification,
        )
        records[case_id]["fingerprint"] = request.fingerprint()
    path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
