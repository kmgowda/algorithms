"""Volume 6, Chapter 18 - Longest Increasing Subsequence: the longest run already in order, with gaps allowed.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import bisect
import itertools
import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]           # Volume 4's returns pile


def lis_table(values: list) -> tuple[int, list, list]:
    """best[i] = longest increasing subsequence ending at position i (Figure 18.2). O(n^2).
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
    """Patience: tops[k] = smallest last value of an increasing subsequence of length k + 1 (Figure 18.3). O(n log n)."""
    tops, history = [], []
    for v in values:
        k = bisect.bisect_left(tops, v)
        if k == len(tops):
            tops.append(v)
        else:
            tops[k] = v
        history.append(list(tops))
    return len(tops), history


def lis_patience(values: list, strict: bool = True) -> tuple[int, list, list]:
    """Patience sorting with back-links (Section 18.5): deal each value onto the leftmost pile whose top is not
    smaller (bisect_left; for a non-decreasing run use bisect_right), remembering the top of the pile to its left.
    Returns (length, one longest increasing subsequence, the piles as lists of values, bottom first)."""
    tops, top_index, piles, link = [], [], [], [-1] * len(values)
    for i, v in enumerate(values):
        k = (bisect.bisect_left if strict else bisect.bisect_right)(tops, v)
        link[i] = top_index[k - 1] if k else -1            # the card this one would follow
        if k == len(tops):
            tops.append(v); top_index.append(i); piles.append([v])
        else:
            tops[k] = v; top_index[k] = i; piles[k].append(v)
    out, i = [], top_index[-1] if top_index else -1
    while i != -1:
        out.append(values[i])
        i = link[i]
    return len(tops), out[::-1], piles


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
