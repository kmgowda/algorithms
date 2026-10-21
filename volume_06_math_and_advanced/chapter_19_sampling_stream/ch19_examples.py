"""Volume 6, Chapter 19 - Sampling a Stream: keep k fair picks from a stream of unknown length (reservoir sampling).

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import random
from collections import Counter


def reservoir(stream, k: int, rng) -> list:
    """Keep the first k; item number i (from 1) replaces a random kept item with probability k / i (Figure 19.2)."""
    if k < 0:
        raise ValueError("k must be 0 or more")
    kept = []
    for i, item in enumerate(stream, start=1):
        if i <= k:
            kept.append(item)
        else:
            j = rng.randrange(i)
            if j < k:
                kept[j] = item
    return kept


def weighted_pick(items: list, weights: list, rng):
    """One pick, chance proportional to weight, in one pass (a reservoir with weights)."""
    total, chosen = 0, None
    for item, w in zip(items, weights):
        if w < 0:
            raise ValueError("weights must not be negative")
        total += w
        if w and rng.random() * total < w:
            chosen = item
    return chosen


if __name__ == "__main__":
    rng = random.Random(19)
    counts = Counter()
    for _ in range(30000):
        counts.update(reservoir(range(10), 3, rng))
    print(sorted(counts.items()))
    print(reservoir(range(2), 5, rng), reservoir([], 3, rng), reservoir(range(100), 0, rng))
    w = Counter(weighted_pick(["a", "b", "c"], [1, 2, 7], rng) for _ in range(10000))
    print(sorted(w.items()))
