"""Tests for tool message parts in the shared runtime."""

from __future__ import annotations

from types import SimpleNamespace

from northstar.runtime import GeminiClient, Message, Part, PromptRequest


def test_tool_parts_fingerprint_and_gemini_contents(monkeypatch):
    request = PromptRequest(
        case_id="runtime/tool-parts",
        messages=[
            Message(
                role="model",
                parts=[Part(kind="tool_call", tool_name="lookup", payload={"id": "ORD-0001"})],
            ),
            Message(
                role="tool",
                parts=[
                    Part(
                        kind="tool_result",
                        tool_name="lookup",
                        payload={"result": "ready"},
                    )
                ],
            ),
        ],
    )
    assert request.fingerprint() == request.fingerprint()

    class FakePart:
        @staticmethod
        def from_function_call(*, name, args):
            return ("call", name, args)

        @staticmethod
        def from_function_response(*, name, response):
            return ("response", name, response)

    class FakeContent:
        def __init__(self, *, role, parts):
            self.role = role
            self.parts = parts

    fake_types = SimpleNamespace(Part=FakePart, Content=FakeContent)
    contents = GeminiClient._contents(GeminiClient.__new__(GeminiClient), request, fake_types)
    assert contents[0].role == "model"
    assert contents[0].parts == [("call", "lookup", {"id": "ORD-0001"})]
    assert contents[1].role == "user"
    assert contents[1].parts == [("response", "lookup", {"result": "ready"})]
