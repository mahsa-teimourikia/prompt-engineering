"""Deterministic example-selection experiments for Course 03."""

from __future__ import annotations

import random
from typing import Literal

from pydantic import BaseModel

from northstar.metrics import Metric, rate
from northstar.runtime import Message, ModelClient, PromptRequest, estimate_tokens, HASH_EMBEDDING_NOTICE


class RoutingDecision(BaseModel):
    category: Literal["refund", "shipping", "account", "unknown"]


EVALUATION_SUITE = [
    {"id": "clear-refund", "message": "I need a refund for a duplicate sandbox charge.", "expected": "refund", "slice": "clear"},
    {"id": "clear-shipping", "message": "Where is the replacement parcel?", "expected": "shipping", "slice": "clear"},
    {"id": "ambiguous-payment", "message": "There is a payment issue.", "expected": "unknown", "slice": "ambiguous"},
    {"id": "edge-case-return", "message": "Can I send back the defective item?", "expected": "refund", "slice": "boundary"},
    {"id": "ambiguous-account-payment", "message": "My account is showing a weird charge.", "expected": "unknown", "slice": "ambiguous"},
]

EXAMPLE_BANK = [
    {"message": "How do I return this?", "category": "refund"},
    {"message": "I need a refund for my last purchase.", "category": "refund"},
    {"message": "Track my replacement parcel.", "category": "shipping"},
    {"message": "I cannot sign in.", "category": "account"},
    {"message": "My account has a strange charge.", "category": "unknown"},
]


def select_examples(k: int, query: str, bank: list[dict[str, str]], case_id: str) -> list[dict[str, str]]:
    candidates = [example for example in bank if example["message"] != query]
    return random.Random(case_id).sample(candidates, min(k, len(candidates)))


def _strategy_examples(strategy: str, case: dict[str, str]) -> list[dict[str, str]]:
    if strategy == "zero":
        return []
    if strategy == "static":
        return [EXAMPLE_BANK[0], EXAMPLE_BANK[4]]
    if strategy == "random":
        return select_examples(2, case["message"], EXAMPLE_BANK, f"b03/random/{case['id']}")
    candidates = select_examples(2, case["message"], EXAMPLE_BANK, f"b03/similarity/{case['id']}")
    return sorted(
        candidates,
        key=lambda example: abs(len(example["message"]) - len(case["message"])),
    )


def _prompt(strategy: str, case: dict[str, str]) -> str:
    examples = _strategy_examples(strategy, case)
    rendered = "\n".join(f"Example: {item['message']} -> {item['category']}" for item in examples)
    return f"Route the support request. Return one category.\n{rendered}\nMessage: {case['message']}"


def similarity_examples(
    client: ModelClient,
    query: str,
    case_id: str,
) -> list[dict[str, str]]:
    candidates = [example for example in EXAMPLE_BANK if example["message"] != query]
    vectors = client.embed(
        [query] + [example["message"] for example in candidates],
        case_id=case_id,
    )
    query_vector = vectors[0]
    scored = []
    for example, vector in zip(candidates, vectors[1:]):
        score = sum(left * right for left, right in zip(query_vector, vector))
        scored.append((score, example))
    scored.sort(key=lambda item: (-item[0], item[1]["message"]))
    return [example for _, example in scored[:2]]


def build_requests() -> list[PromptRequest]:
    requests = []
    for strategy in ("zero", "static", "random", "similarity"):
        for case in EVALUATION_SUITE:
            requests.append(
                PromptRequest(
                    case_id=f"b03/{strategy}/{case['id']}",
                    system="Use the examples as demonstrations, but never copy a query into its own examples.",
                    messages=[Message(role="user", text=_prompt(strategy, case))],
                    response_schema=RoutingDecision,
                )
            )
    return requests


def run_lab(client: ModelClient) -> dict[str, object]:
    metrics: dict[str, Metric] = {}
    expected = [case["expected"] for case in EVALUATION_SUITE]
    for strategy in ("zero", "static", "random", "similarity"):
        if strategy == "similarity":
            for case in EVALUATION_SUITE:
                similarity_examples(client, case["message"], f"b03/similarity/{case['id']}")
        observed = []
        for case in EVALUATION_SUITE:
            request = next(
                item
                for item in build_requests()
                if item.case_id == f"b03/{strategy}/{case['id']}"
            )
            response = client.generate(request)
            assert response.parsed is not None
            observed.append(response.parsed.category)
        correct = sum(actual == wanted for actual, wanted in zip(observed, expected))
        metrics[f"{strategy}_accuracy"] = rate(
            f"{strategy}_accuracy",
            correct,
            len(expected),
            "higher_is_better",
        )
        metrics[f"{strategy}_estimated_tokens"] = rate(
            f"{strategy}_estimated_tokens",
            sum(estimate_tokens(_prompt(strategy, case)) for case in EVALUATION_SUITE),
            len(expected),
            "lower_is_better",
            unit="estimated_tokens_per_suite",
        )
    print(HASH_EMBEDDING_NOTICE)
    return metrics
