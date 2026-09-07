"""A small offline classification demo used by the notebook template."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .contracts import is_abstention, parse_structured
from .metrics import Metric, rate
from .runtime import Message, ModelClient, PromptRequest


class SupportClassification(BaseModel):
    category: Literal["refund", "shipping", "account", "unknown"]


DEMO_CASES = (
    ("b01/baseline/clear-refund", "I need a refund for the duplicate charge.", "refund"),
    ("b01/baseline/clear-shipping", "Where is the replacement shipment?", "shipping"),
    ("b01/baseline/clear-account", "Please unlock my support account.", "account"),
    ("b01/baseline/ambiguous-payment", "There is a payment issue.", "unknown"),
)


def run_demo(client: ModelClient) -> dict[str, Metric]:
    """Classify four synthetic tickets and return accuracy metrics."""

    correct = 0
    abstentions = 0
    for case_id, text, expected in DEMO_CASES:
        request = PromptRequest(
            case_id=case_id,
            system="Classify the ticket into one supported category.",
            messages=[Message(role="user", text=text)],
            response_schema=SupportClassification,
        )
        response = client.generate(request)
        result = parse_structured(SupportClassification, response.text)
        if result.ok and result.value.category == expected:
            correct += 1
        if result.ok and is_abstention(result.value.category):
            abstentions += 1
    return {
        "classification_accuracy": rate(
            "classification_accuracy",
            correct,
            len(DEMO_CASES),
            "higher_is_better",
        ),
        "abstention_rate": rate(
            "abstention_rate",
            abstentions,
            len(DEMO_CASES),
            "lower_is_better",
        ),
    }
