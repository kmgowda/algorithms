"""Volume 5, Chapter 10 - Longest Increasing Subsequence: the longest run already in order, with gaps allowed.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import bisect
import itertools
import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]           # Volume 3's returns pile


def lis_table(values: list) -> tuple[int, list, list]:
    """best[i] = longest increasing subsequence ending at position i (Figure 10.2). O(n^2).
    Returns (length, one such subsequence, best)."""
    n = len(values)
    best, prev = [1] * n, [-1] * n
    for i in range(n):
        for j in range(i):
            if values[j] < values[i] and best[j] + 1 > best[i]:
                best[i], prev[i] = best[j] + 1, j
    if not n:
        return 0, [], []
    i = max(range(n), key=lambda k: best[k])
    out = []
    while i != -1:
        out.append(values[i])
        i = prev[i]
    return max(best), out[::-1], best


def lis_piles(values: list) -> tuple[int, list]:
    """Patience: tops[k] = smallest last value of an increasing subsequence of length k + 1 (Figure 10.3). O(n log n)."""
    tops, history = [], []
    for v in values:
        k = bisect.bisect_left(tops, v)
        if k == len(tops):
            tops.append(v)
        else:
            tops[k] = v
        history.append(list(tops))
    return len(tops), history


def brute(values: list) -> int:
    for k in range(len(values), 0, -1):
        if any(all(a < b for a, b in zip(c, c[1:])) for c in itertools.combinations(values, k)):
            return k
    return 0


if __name__ == "__main__":
    print(lis_table(PILE))
    print(lis_piles(PILE))
    r = random.Random(10)
    for n in (1000, 4000):
        v = [r.random() for _ in range(n)]
        t = time.perf_counter(); a = lis_table(v)[0]; t1 = time.perf_counter() - t
        t = time.perf_counter(); b = lis_piles(v)[0]; t2 = time.perf_counter() - t
        print(n, a, b, round(t1 * 1000), round(t2 * 1000, 1))
