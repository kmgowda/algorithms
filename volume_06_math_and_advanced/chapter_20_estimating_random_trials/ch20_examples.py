"""Volume 6, Chapter 20 - Estimating with Random Trials: Monte Carlo estimates and how accurate they are.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

import math
import random


def estimate_pi(trials: int, rng) -> float:
    """Darts at a unit square: the fraction inside the quarter circle is pi/4 (Figure 20.1)."""
    if trials <= 0:
        raise ValueError("at least one trial is needed")
    inside = sum(1 for _ in range(trials) if rng.random() ** 2 + rng.random() ** 2 <= 1)
    return 4 * inside / trials


def shared_birthday(people: int, trials: int, rng) -> float:
    """Fraction of trial groups in which two people share a birthday (365 days)."""
    hits = 0
    for _ in range(trials):
        days = [rng.randrange(365) for _ in range(people)]
        hits += len(set(days)) < people
    return hits / trials


def shared_birthday_exact(people: int) -> float:
    p = 1.0
    for i in range(people):
        p *= (365 - i) / 365
    return 1 - p


def queue_wait(trials: int, rng) -> float:
    """Average wait at a desk: a visitor arrives each minute with chance 0.5; serving takes 1 or 2 minutes equally often.
    The answer has no simple formula, so we estimate it."""
    total_wait, served = 0, 0
    for _ in range(trials):
        free_at, wait = 0, 0
        for minute in range(60):
            if rng.random() < 0.5:
                start = max(minute, free_at)
                wait += start - minute
                free_at = start + rng.choice((1, 2))
                served += 1
        total_wait += wait
    return total_wait / served


if __name__ == "__main__":
    rng = random.Random(20)
    for n in (100, 10_000, 1_000_000):
        e = estimate_pi(n, rng)
        print(n, e, round(abs(e - math.pi), 4))
    print(shared_birthday(23, 20000, rng), round(shared_birthday_exact(23), 4), round(shared_birthday_exact(50), 4))
    print(round(queue_wait(5000, rng), 3))
