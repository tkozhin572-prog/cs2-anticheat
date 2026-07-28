from __future__ import annotations

from math import sqrt
from statistics import mean


def safe_mean(values: list[float]) -> float:
    return mean(values) if values else 0.0


def population_std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    return sqrt(sum((value - avg) ** 2 for value in values) / len(values))


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def ratio(part: int, total: int) -> float:
    return part / total if total else 0.0
