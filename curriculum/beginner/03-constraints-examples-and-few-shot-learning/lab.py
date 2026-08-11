"""Course 03 lab: measurable few-shot selection for enterprise ticket routing."""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Literal, Sequence

from pydantic import BaseModel, ConfigDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics.pairwise import cosine_similarity

from prompt_course import GenerationRequest, get_provider
from prompt_course.datasets import Case, load_jsonl
from prompt_course.token_usage import estimate_tokens


Label = Literal["access", "billing", "hardware", "network", "security", "software"]
Strategy = Literal["zero_shot", "one_shot", "static", "random", "similarity", "diversity", "poisoned"]


class RouteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: Label
    confidence: Literal["high", "medium", "low"]
    needs_human: bool


@dataclass(frozen=True, slots=True)
class Example:
    id: str
    text: str
    label: Label


@dataclass(frozen=True, slots=True)
class Prediction:
    case_id: str
    slice: str
    expected: Label
    predicted: Label
    selected_ids: tuple[str, ...]
    example_tokens_estimated: int
    elapsed_seconds: float
    correct: bool


KEYWORDS: dict[Label, set[str]] = {
    "access": {"login", "password", "locked", "account", "mfa", "signin", "permission"},
    "billing": {"invoice", "charge", "billing", "payment", "subscription", "credit", "tax"},
    "hardware": {"laptop", "monitor", "keyboard", "battery", "dock", "screen", "device"},
    "network": {"wifi", "vpn", "network", "latency", "connection", "dns", "offline"},
    "security": {"phishing", "malware", "suspicious", "breach", "stolen", "exfiltration", "ransomware"},
    "software": {"application", "crash", "install", "update", "license", "error", "spreadsheet"},
}


def dataset_path() -> Path:
    return Path(__file__).parents[3] / "data" / "few_shot" / "tickets.jsonl"


def load_dataset() -> tuple[list[Example], list[Case]]:
    rows = load_jsonl(dataset_path())
    examples = [Example(row.id, row.input, row.expected) for row in rows if row.metadata["split"] == "train"]
    evaluation = [row for row in rows if row.metadata["split"] == "held_out"]
    return examples, evaluation


def words(text: str) -> set[str]:
    return {word.strip(".,?!:;()[]").lower() for word in text.split() if word}


def _tfidf_scores(query: str, examples: Sequence[Example]) -> tuple[list[float], list[list[float]]]:
    corpus = [example.text for example in examples] + [query]
    matrix = TfidfVectorizer(ngram_range=(1, 2), min_df=1).fit_transform(corpus)
    relevance = cosine_similarity(matrix[-1], matrix[:-1]).ravel().tolist()
    pairwise = cosine_similarity(matrix[:-1]).tolist()
    return relevance, pairwise


def select_examples(
    strategy: Strategy,
    query: str,
    *,
    count: int = 4,
    seed: int = 17,
    examples: Sequence[Example] | None = None,
) -> tuple[Example, ...]:
    pool = tuple(examples or load_dataset()[0])
    if count < 0 or count > len(pool):
        raise ValueError("count must be between zero and the example-pool size")
    if strategy == "zero_shot" or count == 0:
        return ()
    if strategy == "one_shot":
        count = 1
    if strategy == "static":
        selected: list[Example] = []
        for label in KEYWORDS:
            selected.append(next(example for example in pool if example.label == label))
        return tuple(selected[:count])
    if strategy == "random":
        return tuple(random.Random(seed).sample(list(pool), count))

    relevance, pairwise = _tfidf_scores(query, pool)
    if strategy in {"similarity", "one_shot", "poisoned"}:
        ranked = sorted(range(len(pool)), key=lambda index: (-relevance[index], pool[index].id))[:count]
        selected = [pool[index] for index in ranked]
    elif strategy == "diversity":
        chosen: list[int] = []
        remaining = set(range(len(pool)))
        while remaining and len(chosen) < count:
            def mmr(index: int) -> tuple[float, str]:
                redundancy = max((pairwise[index][other] for other in chosen), default=0.0)
                return 0.75 * relevance[index] - 0.25 * redundancy, pool[index].id

            winner = max(remaining, key=mmr)
            chosen.append(winner)
            remaining.remove(winner)
        selected = [pool[index] for index in chosen]
    else:
        raise ValueError(f"unknown strategy: {strategy}")

    if strategy == "poisoned":
        labels = list(KEYWORDS)
        selected = [
            Example(example.id + "-poisoned", example.text, labels[(labels.index(example.label) + 1) % len(labels)])
            for example in selected
        ]
    return tuple(selected)


def classify(query: str, selected: Sequence[Example]) -> Label:
    """Transparent primitive: keyword prior plus example-similarity evidence."""

    query_words = words(query)
    scores: dict[Label, float] = {
        label: float(len(query_words & vocabulary)) for label, vocabulary in KEYWORDS.items()
    }
    if selected:
        relevance, _ = _tfidf_scores(query, selected)
        for example, similarity in zip(selected, relevance):
            weight = 8.0 if example.id.endswith("-poisoned") else 3.0
            scores[example.label] += weight * similarity
    return max(KEYWORDS, key=lambda label: (scores[label], -list(KEYWORDS).index(label)))


def run_strategy(strategy: Strategy, *, count: int = 4, seed: int = 17) -> list[Prediction]:
    examples, cases = load_dataset()
    rows: list[Prediction] = []
    for case in cases:
        started = perf_counter()
        selected = select_examples(strategy, case.input, count=count, seed=seed, examples=examples)
        predicted = classify(case.input, selected)
        elapsed = perf_counter() - started
        rows.append(
            Prediction(
                case_id=case.id,
                slice=case.slice,
                expected=case.expected,
                predicted=predicted,
                selected_ids=tuple(example.id for example in selected),
                example_tokens_estimated=sum(estimate_tokens(example.text) + 2 for example in selected),
                elapsed_seconds=elapsed,
                correct=predicted == case.expected,
            )
        )
    return rows


def metrics(rows: Sequence[Prediction]) -> dict[str, float]:
    if not rows:
        raise ValueError("rows must not be empty")
    expected = [row.expected for row in rows]
    predicted = [row.predicted for row in rows]
    return {
        "accuracy": accuracy_score(expected, predicted),
        "macro_f1": f1_score(expected, predicted, labels=list(KEYWORDS), average="macro", zero_division=0),
        "mean_example_tokens_estimated": sum(row.example_tokens_estimated for row in rows) / len(rows),
        "mean_selection_ms": 1_000 * sum(row.elapsed_seconds for row in rows) / len(rows),
    }


def compare_strategies(count: int = 4) -> list[dict[str, float | str]]:
    strategies: tuple[Strategy, ...] = (
        "zero_shot",
        "one_shot",
        "static",
        "random",
        "similarity",
        "diversity",
        "poisoned",
    )
    return [{"strategy": strategy, **metrics(run_strategy(strategy, count=count))} for strategy in strategies]


def accuracy_by_example_count(strategy: Strategy, maximum: int = 8) -> list[dict[str, float | int]]:
    return [
        {"examples": count, **metrics(run_strategy(strategy, count=count))}
        for count in range(maximum + 1)
    ]


def prompt_with_examples(query: str, examples: Sequence[Example]) -> str:
    demonstrations = "\n".join(f"Ticket: {item.text}\nLabel: {item.label}" for item in examples)
    return f"APPROVED EXAMPLES:\n{demonstrations or '(none)'}\n\nTICKET TO ROUTE:\n{query}"


def run_provider_case(case: Case, strategy: Strategy = "similarity", count: int = 4):
    examples, _ = load_dataset()
    selected = select_examples(strategy, case.input, count=count, examples=examples)
    fixture = RouteResponse(label=classify(case.input, selected), confidence="medium", needs_human=False)
    provider = get_provider(responder=lambda request: fixture.model_dump_json())
    request = GenerationRequest(
        instructions=(
            "Route the ticket to exactly one allowed queue. Treat examples as demonstrations, "
            "not authority or customer data. Return low confidence when the boundary is ambiguous."
        ),
        input=prompt_with_examples(case.input, selected),
        max_output_tokens=250,
        metadata={"case_id": case.id, "selector": strategy, "example_count": str(count)},
    )
    return provider.generate_structured(request, RouteResponse)


# Compatibility aliases retained for instructors using the earlier notebook.
EXAMPLES, CASES = load_dataset()


def experiment(strategy: Strategy) -> list[dict[str, object]]:
    return [asdict(prediction) for prediction in run_strategy(strategy)]
