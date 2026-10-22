"""Volume 3, Chapter 6 - Why Binary Search Trees Go Wrong.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import math
import random


def insert_all(keys) -> tuple[int, int]:
    """Insert keys into a plain BST (iteratively). Returns (height, total comparisons)."""
    left, right, depth = {}, {}, {}
    root = None
    comparisons = 0
    for k in keys:
        if root is None:
            root, depth[k] = k, 0
            continue
        n = root
        while True:
            comparisons += 1
            side = left if k < n else right
            if n not in side:
                side[n] = k
                depth[k] = depth[n] + 1
                break
            n = side[n]
    return (max(depth.values()) if depth else -1), comparisons


def average_found_comparisons(keys) -> float:
    """Practice Problem 2: comparisons for a successful search, averaged over every key (depth + 1)."""
    left, right, depth, root = {}, {}, {}, None
    for k in keys:
        if root is None:
            root, depth[k] = k, 0
            continue
        n = root
        while True:
            side = left if k < n else right
            if n not in side:
                side[n], depth[k] = k, depth[n] + 1
                break
            n = side[n]
    return sum(d + 1 for d in depth.values()) / len(depth) if depth else 0.0


def median_first(lo: int, hi: int) -> list[int]:
    """An insertion order that builds the shortest tree of lo..hi: each range's middle comes first."""
    if lo > hi:
        return []
    m = (lo + hi) // 2
    return [m] + median_first(lo, m - 1) + median_first(m + 1, hi)


def average_random_height(n: int, trials: int = 20) -> float:
    """Figures 6.3 and 6.7: average height over 20 random insertion orders."""
    return sum(insert_all(random.Random(s).sample(range(10 ** 6), n))[0] for s in range(trials)) / trials


def deliveries(batches: int = 50, size: int = 20, seed: int = 1) -> int:
    """Section 6.7: increasing batches, each shuffled. Returns the tree height."""
    rng = random.Random(seed)
    keys = []
    for b in range(batches):
        batch = list(range(b * size, (b + 1) * size))
        rng.shuffle(batch)
        keys += batch
    return insert_all(keys)[0]


if __name__ == "__main__":
    for n in (10, 100, 1000):
        print(n, average_random_height(n), insert_all(range(n))[0], round(math.log2(n), 1))
    print(insert_all(range(1000))[1], deliveries(), round(average_random_height(10_000), 1))
    print(insert_all([47, 12, 25, 31, 58, 63, 70]), average_found_comparisons(range(1, 101)),
          round(average_found_comparisons(median_first(1, 100)), 1))
