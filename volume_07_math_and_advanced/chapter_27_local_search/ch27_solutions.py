"""Volume 7, Chapter 27 - Thinking Problems.

Problem 1: max-cut local search makes at most m moves (each move raises the cut by at least 1; the cut is at most m).
Problem 2: how many independent restarts give a 99% chance of hitting a target found with chance p per run.
Problem 3: the sign error exp(+delta / T) accepts every worse move, turning annealing into a random walk.
"""

from __future__ import annotations

import math


def restarts_needed(p: float, confidence: float = 0.99) -> int:
    """Smallest r with 1 - (1 - p)^r >= confidence."""
    if not 0 < p <= 1 or not 0 < confidence < 1:
        raise ValueError("need 0 < p <= 1 and 0 < confidence < 1")
    if p == 1:
        return 1
    return math.ceil(math.log(1 - confidence) / math.log(1 - p))


def accept_probability(delta: float, temp: float) -> float:
    """Correct rule: always accept improvements; accept a change that adds delta > 0 with chance e^(-delta/T)."""
    return 1.0 if delta <= 0 else math.exp(-delta / temp)


def buggy_accept_probability(delta: float, temp: float) -> float:
    return 1.0 if delta <= 0 else min(1.0, math.exp(delta / temp))   # sign error: e^(+delta/T) >= 1


if __name__ == "__main__":
    print(restarts_needed(0.3), restarts_needed(0.5), restarts_needed(0.05))
    print(round(accept_probability(10, 10), 3), buggy_accept_probability(10, 10))
