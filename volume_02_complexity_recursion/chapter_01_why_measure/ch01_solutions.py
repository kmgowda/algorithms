"""Volume 2, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

import math


def predict_time(measured_seconds: float, measured_n: int, new_n: int, exponent: float) -> float:
    """Exercise 2: if time grows like n^exponent, scale a measurement to a new size."""
    return measured_seconds * (new_n / measured_n) ** exponent


def triple_loop_steps(n: int) -> int:
    """Exercise 3: every group of three different items (i < j < k)."""
    steps = 0
    for i in range(n):
        for j in range(i + 1, n):
            for _ in range(j + 1, n):
                steps += 1
    return steps


def classify_ratio(ratio: float) -> str:
    """Exercise 4: name the growth suggested by a doubling ratio."""
    exponent = math.log2(ratio) if ratio > 0 else 0.0
    if exponent < 0.5:
        return "constant or logarithmic"
    if exponent < 1.5:
        return "linear (or n log n)"
    if exponent < 2.5:
        return "quadratic"
    return "cubic or worse"


def steps_for_report(students: int, subjects: int) -> int:
    """Exercise 5: a report card loops over students, and for each over subjects."""
    return students * subjects


if __name__ == "__main__":
    print(predict_time(2.0, 10_000, 1_000_000, 2), predict_time(2.0, 10_000, 1_000_000, 1))
    print(triple_loop_steps(10), classify_ratio(4.1), steps_for_report(500, 6))
