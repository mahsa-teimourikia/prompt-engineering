"""Tests for the Course 11 offline lab."""

import importlib.util
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from northstar.runtime import ReplayClient

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/11-tool-calling-and-tool-interface-design/lab11.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab11", PATH)
assert SPEC and SPEC.loader
lab11 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab11)


def test_course_11_validation_authorization_and_unknown_tool():
    results = lab11.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["unauthorized_executions"].numerator == 0
    with pytest.raises(ValidationError):
        lab11.OrderStatusArgs.model_validate({"order_id": "999"})
    with pytest.raises(lab11.UnknownToolError):
        lab11.dispatch("delete_order", {"order_id": "ORD-999"})
