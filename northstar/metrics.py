"""Small metric primitives that retain numerators and denominators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Literal, TypeVar


Direction = Literal["higher_is_better", "lower_is_better"]
T = TypeVar("T")


@dataclass(frozen=True)
class Metric:
    name: str
    numerator: int
    denominator: int
    unit: str
    direction: Direction
    slice: str = "all"

    @property
    def value(self) -> float | None:
        return (
            None
            if self.denominator == 0
            else self.numerator / self.denominator
        )


def rate(
    name: str,
    hits: int,
    total: int,
    direction: Direction,
    unit: str = "ratio",
    slice: str = "all",
) -> Metric:
    return Metric(name, hits, total, unit, direction, slice)


def by_slice(
    records: Iterable[T],
    key: Callable[[T], str] | str,
    predicate: Callable[[T], bool],
    name: str,
    direction: Direction,
) -> list[Metric]:
    selector = key if callable(key) else lambda record: record[key]
    grouped: dict[str, list[T]] = {}
    for record in records:
        grouped.setdefault(selector(record), []).append(record)
    return [
        rate(name, sum(predicate(record) for record in group), len(group), direction, slice=slice_name)
        for slice_name, group in sorted(grouped.items())
    ]


def render(metrics: Iterable[Metric]) -> str:
    """Render metrics as a markdown table including numerator/denominator."""

    rows = [
        "| Metric | Slice | Numerator | Denominator | Value | Unit | Direction |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for metric in metrics:
        value = "—" if metric.value is None else f"{metric.value:.3f}"
        rows.append(
            f"| {metric.name} | {metric.slice} | {metric.numerator} | "
            f"{metric.denominator} | {value} | {metric.unit} | {metric.direction} |"
        )
    return "\n".join(rows)
