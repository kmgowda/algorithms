"""Volume 14, Chapter 7 - Probability for Algorithms.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Iterable, TypeVar

T = TypeVar("T")


def expected_value(outcomes: dict[float, float]) -> float:
    """Sum of value x probability."""
    return sum(v * p for v, p in outcomes.items())


def simulate_mean(roll, trials: int, rng: random.Random) -> float:
    """Estimate an expected value by averaging many random trials."""
    return sum(roll(rng) for _ in range(trials)) / trials


def fisher_yates(items: list[T], rng: random.Random) -> list[T]:
    """LeetCode 384: a uniformly random shuffle - swap each position with a random position at or before it."""
    out = list(items)
    for i in range(len(out) - 1, 0, -1):
        j = rng.randint(0, i)
        out[i], out[j] = out[j], out[i]
    return out


def naive_shuffle(items: list[T], rng: random.Random) -> list[T]:
    """A common BUG: swapping with ANY position gives n^n equally likely runs, which can't split evenly over n! orders."""
    out = list(items)
    for i in range(len(out)):
        j = rng.randint(0, len(out) - 1)
        out[i], out[j] = out[j], out[i]
    return out


def reservoir_sample(stream: Iterable[T], k: int, rng: random.Random) -> list[T]:
    """LeetCode 382/398: k uniform random items from a stream of unknown length, in one pass and O(k) memory.
    Item number i (1-based) replaces a random slot with probability k / i."""
    sample: list[T] = []
    for i, item in enumerate(stream, 1):
        if i <= k:
            sample.append(item)
        else:
            j = rng.randint(1, i)
            if j <= k:
                sample[j - 1] = item
    return sample


def monte_carlo_pi(points: int, rng: random.Random) -> float:
    """Throw random points into a square; the fraction landing inside the quarter circle approaches pi / 4."""
    inside = sum(1 for _ in range(points) if rng.random() ** 2 + rng.random() ** 2 <= 1)
    return 4 * inside / points


def birthday_collision(people: int, days: int = 365) -> float:
    """Probability that at least two of `people` share a birthday: 1 - (365/365)(364/365)...(365-n+1)/365."""
    p_distinct = 1.0
    for i in range(people):
        p_distinct *= (days - i) / days
    return 1 - p_distinct


def ab_test_sample(user_ids: list[int], percent: int, rng: random.Random) -> list[int]:
    """Industry example: pick a random percentage of users for an experiment, each user equally likely."""
    k = len(user_ids) * percent // 100
    return reservoir_sample(user_ids, k, rng)


if __name__ == "__main__":
    rng = random.Random(1)
    die = {v: 1 / 6 for v in range(1, 7)}
    print("expected die:", expected_value(die), "| simulated:", round(simulate_mean(lambda r: r.randint(1, 6), 100000, rng), 3))
    counts_fy = Counter(tuple(fisher_yates([1, 2, 3], rng)) for _ in range(60000))
    counts_bad = Counter(tuple(naive_shuffle([1, 2, 3], rng)) for _ in range(60000))
    print("Fisher-Yates:", sorted(counts_fy.values()), "| naive:", sorted(counts_bad.values()))
    print("reservoir:", reservoir_sample(range(1, 1001), 5, rng))
    print("pi estimates:", [round(monte_carlo_pi(n, rng), 4) for n in (100, 10000, 1000000)], "true", round(math.pi, 4))
    print("birthday 23 people:", round(birthday_collision(23), 3), "| 50 people:", round(birthday_collision(50), 3))
