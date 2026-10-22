"""Volume 7, Chapter 17 - Thinking Problem 2: a fair sample of k entries out of n, in O(k) time and memory
(Robert Floyd's method), with no list of all n entries.

Run:  python3 ch17_solutions.py
"""

from __future__ import annotations

import random


def floyd_sample(n: int, k: int, rng) -> set:
    """A uniformly random k-element subset of range(n): for j = n-k .. n-1, draw t in 0..j; take t if it is new,
    otherwise take j (which cannot have been taken yet)."""
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")
    chosen = set()
    for j in range(n - k, n):
        t = rng.randrange(j + 1)
        chosen.add(j if t in chosen else t)
    return chosen


if __name__ == "__main__":
    print(sorted(floyd_sample(10 ** 9, 3, random.Random(17))))
