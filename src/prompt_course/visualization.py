"""Accessible plotting helpers for measured lab results."""

from __future__ import annotations

from collections.abc import Iterable


def comparison_bars(
    labels: Iterable[str],
    values: Iterable[float],
    *,
    title: str,
    metric_label: str,
):
    import matplotlib.pyplot as plt

    label_list = list(labels)
    value_list = list(values)
    if not label_list or len(label_list) != len(value_list):
        raise ValueError("labels and values must be non-empty and the same length")
    figure, axis = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
    bars = axis.bar(label_list, value_list, color="#2F6FED")
    axis.set_title(title)
    axis.set_ylabel(metric_label)
    axis.set_xlabel("Strategy")
    axis.bar_label(bars, fmt="%.3g", padding=3)
    axis.grid(axis="y", alpha=0.25)
    return figure, axis
