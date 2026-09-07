"""Tests for the Course 11 offline lab."""

import importlib.util
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from northstar.runtime import ReplayClient
from northstar.security import Decision, Principal

ROOT = Path(__file__).parents[1]
PATH = ROOT / "curriculum/intermediate/11-tool-calling-and-tool-interface-design/lab11.py"
SPEC = importlib.util.spec_from_file_location("intermediate_lab11", PATH)
assert SPEC and SPEC.loader
lab11 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab11)


def test_course_11_validation_authorization_and_unknown_tool():
    results = lab11.run_lab(ReplayClient(PATH.parent / "fixtures/replays.json"))
    assert results["unauthorized_executions"].numerator == 0
    assert results["unauthorized_executions"].denominator == 4
    with pytest.raises(ValidationError):
        lab11.OrderStatusArgs.model_validate({"order_id": "999"})
    with pytest.raises(lab11.UnknownToolError):
        lab11.dispatch("delete_order", {"order_id": "ORD-999"})


def test_course_11_denied_authorization_skips_execution(monkeypatch):
    events = []
    counter = [0]
    principal = Principal(user_id="USER-0001", tenant="tenant-synthetic-a", roles={"support_agent"})
    monkeypatch.setattr(
        lab11,
        "authorize",
        lambda *_args, **_kwargs: Decision(allowed=False, reason_code="test_denied"),
    )
    result = lab11.execute(
        principal,
        {"order_id": "ORD-999"},
        case_id="denied",
        execution_counter=counter,
        events=events,
    )
    assert result == {"error": "not_authorized", "reason_code": "test_denied"}
    assert counter == [0]
    assert events == [{"case_id": "denied", "authorized": False, "executed": False}]
    assert lab11.unauthorized_execution_metric(events, 1).numerator == 0


def test_course_11_metric_catches_execute_before_authorize():
    broken_events = [{"case_id": "broken", "authorized": False, "executed": True}]
    assert lab11.unauthorized_execution_metric(broken_events, 1).numerator == 1
