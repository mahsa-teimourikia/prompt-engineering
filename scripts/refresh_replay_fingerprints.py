"""Refresh demo replay fingerprints from the real PromptRequest implementation."""

from __future__ import annotations

import json
import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from northstar.demo import DEMO_CASES, SupportClassification
from northstar.runtime import Message, PromptRequest


def refresh_demo() -> None:
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


def refresh_course(course_dir: Path) -> None:
    lab_paths = sorted(course_dir.glob("lab*.py"))
    if len(lab_paths) != 1:
        raise ValueError(f"expected one lab module in {course_dir}")
    spec = importlib.util.spec_from_file_location("course_lab", lab_paths[0])
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {lab_paths[0]}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    sys.path.insert(0, str(course_dir))
    spec.loader.exec_module(module)
    requests = module.build_requests()
    replay_path = course_dir / "fixtures" / "replays.json"
    records = json.loads(replay_path.read_text(encoding="utf-8"))
    for request in requests:
        if request.case_id not in records:
            raise KeyError(f"missing replay for {request.case_id}")
        records[request.case_id]["fingerprint"] = request.fingerprint()
    extra = set(records) - {request.case_id for request in requests}
    if extra:
        raise KeyError(f"replays without requests: {sorted(extra)}")
    replay_path.write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", type=Path)
    arguments = parser.parse_args()
    if arguments.course:
        refresh_course((ROOT / arguments.course).resolve())
    else:
        refresh_demo()


if __name__ == "__main__":
    main()
