"""Replay-backed multimodal invoice extraction and reconciliation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw
from pydantic import BaseModel, Field

from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, Part, PromptRequest


COURSE_DIR = Path(__file__).parent
IMAGE_PATH = COURSE_DIR / "fixtures/synthetic_invoice.png"
if not IMAGE_PATH.exists():
    IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (640, 360), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 40), "NORTHSTAR SYNTHETIC INVOICE", fill="black")
    draw.text((40, 100), "Invoice: INV-0007", fill="black")
    draw.text((40, 160), "Total due: $500.00", fill="black")
    image.save(IMAGE_PATH)

CASES = json.loads((COURSE_DIR / "fixtures/cases.json").read_text())


class InvoiceExtraction(BaseModel):
    is_contradictory: bool = Field(
        description=(
            "Set to True if the amount claimed in the user's text contradicts "
            "the amount visible in the image."
        )
    )
    extracted_amount: float | None = Field(
        default=None,
        description="The amount visible in the image. Return null if there is a contradiction."
    )
    reasoning: str = Field(
        default="",
        description="Explain why you flagged this as contradictory or not."
    )
    invoice_id: str | None = None
    total: float | None = None


def build_requests() -> list[PromptRequest]:
    return [
        PromptRequest(
            case_id=f"i12/{case['id']}",
            system="",
            messages=[
                Message(
                    role="user",
                    text=case["prompt_template"].format(message=case["message"]),
                    parts=[Part(kind="image", path="fixtures/synthetic_invoice.png")],
                )
            ],
            response_schema=InvoiceExtraction,
        )
        for case in CASES
    ]


def claimed_amount(text: str) -> float | None:
    match = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
    return float(match.group(1)) if match else None


def route(extraction: InvoiceExtraction, claimed: float | None) -> Literal["human_review", "auto_process"]:
    extracted_amount = (
        extraction.extracted_amount
        if extraction.extracted_amount is not None
        else extraction.total
    )
    if (
        extraction.is_contradictory
        or claimed != extracted_amount
        or extracted_amount is None
    ):
        return "human_review"
    return "auto_process"


def run_lab(client: ModelClient) -> dict[str, Metric | str]:
    decisions = []
    for case in CASES:
        response = client.generate(next(item for item in build_requests() if item.case_id == f"i12/{case['id']}"))
        extraction = response.parsed or InvoiceExtraction.model_validate_json(response.text)
        decisions.append(route(extraction, claimed_amount(case["message"])))
    return {
        "contradictions_routed": rate(
            "contradictions_routed",
            sum(decision == "human_review" for decision in decisions),
            len(CASES),
            "higher_is_better",
        ),
        "decisions": ",".join(decisions),
    }
