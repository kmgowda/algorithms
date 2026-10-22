"""Volume 6, Chapter 22 - Thinking Problems.

Problem 1: reading only the previous row makes row i the cheapest cost with at most i legs (checked by brute force).
Problem 2: walks of exactly k legs from the start to every depot, by one table row per leg.
Problem 3: updating the row in place lets one round use several legs: with k = 1 the buggy table reaches D and E.
"""

from __future__ import annotations

import itertools


def brute_at_most(vertices, edges, start, k) -> dict:
    inf = float("inf")
    best = {v: inf for v in vertices}
    best[start] = 0
    for m in range(1, k + 1):
        for seq in itertools.product(edges, repeat=m):
            if seq[0][0] == start and all(seq[i][1] == seq[i + 1][0] for i in range(m - 1)):
                cost = sum(w for *_, w in seq)
                best[seq[-1][1]] = min(best[seq[-1][1]], cost)
    return best


def walks_exactly(vertices, edges, start, k) -> dict:
    row = {v: (1 if v == start else 0) for v in vertices}
    for _ in range(k):
        nxt = {v: 0 for v in vertices}
        for a, b, _ in edges:
            nxt[b] += row[a]
        row = nxt
    return row


def at_most_k_in_place(vertices, edges, start, k) -> dict:
    inf = float("inf")
    cur = {v: (0 if v == start else inf) for v in vertices}
    for _ in range(k):
        for a, b, w in edges:                       # the bug: reads values changed in this same round
            if cur[a] + w < cur[b]:
                cur[b] = cur[a] + w
    return cur


if __name__ == "__main__":
    from ch22_examples import DEPOTS, LEGS, at_most_k
    print(at_most_k(DEPOTS, LEGS, "A", 1)[-1], at_most_k_in_place(DEPOTS, LEGS, "A", 1))
    print(walks_exactly(DEPOTS, LEGS, "A", 2), walks_exactly(DEPOTS, LEGS, "A", 3))
