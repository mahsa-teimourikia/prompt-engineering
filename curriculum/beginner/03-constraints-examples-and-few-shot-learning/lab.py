"""Offline few-shot selection experiments for Course 03."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Literal


Label = Literal["refund", "shipping", "account", "unknown"]


@dataclass(frozen=True)
class Example:
    text: str
    label: Label


@dataclass(frozen=True)
class Case:
    text: str
    expected: Label


EXAMPLES = (
    Example("Where is my delivery?", "shipping"),
    Example("Can I return an item that arrived yesterday?", "refund"),
    Example("Change the email on my profile.", "account"),
    Example("I was charged and need help.", "unknown"),
    Example("Track package 99.", "shipping"),
    Example("The product is damaged; how do I return it?", "refund"),
)

CASES = (
    Case("My package has not arrived.", "shipping"),
    Case("I want to send back the product.", "refund"),
    Case("Update my account email address.", "account"),
    Case("There is a payment problem.", "unknown"),
)


def words(text: str) -> set[str]:
    return {word.strip(".,?!").lower() for word in text.split() if word}


def similarity(text: str, example: Example) -> float:
    left, right = words(text), words(example.text)
    return len(left & right) / max(1, len(left | right))


def select_examples(strategy: str, query: str, count: int = 2, seed: int = 3) -> tuple[Example, ...]:
    if strategy == "none":
        return ()
    if strategy == "static":
        return EXAMPLES[:count]
    if strategy == "random":
        return tuple(Random(seed).sample(list(EXAMPLES), count))
    ranked = sorted(EXAMPLES, key=lambda item: similarity(query, item), reverse=True)
    if strategy == "similarity":
        return tuple(ranked[:count])
    if strategy == "diversity":
        selected: list[Example] = []
        for item in ranked:
            if item.label not in {chosen.label for chosen in selected}:
                selected.append(item)
            if len(selected) == count:
                return tuple(selected)
        return tuple(selected)
    raise ValueError(f"unknown strategy: {strategy}")


def classify(query: str, selected: tuple[Example, ...]) -> Label:
    """Transparent baseline: selected evidence may help or bias the label."""
    query_words = words(query)
    lexical = {
        "refund": {"return", "back", "damaged", "product"},
        "shipping": {"package", "delivery", "arrived", "track"},
        "account": {"account", "email", "profile", "address"},
    }
    scores = {label: len(query_words & tokens) for label, tokens in lexical.items()}
    for example in selected:
        scores[example.label] += 2 * similarity(query, example)
    highest = max(scores.values())
    candidates = [label for label, score in scores.items() if score == highest and score > 0]
    return candidates[0] if len(candidates) == 1 else "unknown"


def experiment(strategy: str) -> list[dict[str, object]]:
    rows = []
    for case in CASES:
        selected = select_examples(strategy, case.text)
        predicted = classify(case.text, selected)
        rows.append({
            "case": case.text,
            "expected": case.expected,
            "predicted": predicted,
            "correct": predicted == case.expected,
            "examples": tuple((item.text, item.label) for item in selected),
            "token_estimate": sum(len(item.text.split()) for item in selected),
        })
    return rows


def metrics(rows: list[dict[str, object]]) -> dict[str, float]:
    return {
        "accuracy": sum(bool(row["correct"]) for row in rows) / len(rows),
        "mean_example_tokens": sum(int(row["token_estimate"]) for row in rows) / len(rows),
    }
