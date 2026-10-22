"""Volume 5, Chapter 13 - DP over Subsets: the van's round by Held-Karp, one set of visited branches at a time.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import itertools
import math
import random

BRANCHES = ["Library", "North", "East", "South", "West"]      # Volume 4, Chapter 17's van round
TRAVEL = {("Library", "North"): 2, ("Library", "East"): 9, ("Library", "South"): 10, ("Library", "West"): 7,
          ("North", "East"): 6, ("North", "South"): 4, ("North", "West"): 3, ("East", "South"): 8,
          ("East", "West"): 5, ("South", "West"): 1}


def matrix(names: list, travel: dict) -> list:
    n = len(names)
    d = [[0] * n for _ in range(n)]
    for (a, b), w in travel.items():
        i, j = names.index(a), names.index(b)
        d[i][j] = d[j][i] = w
    return d


def held_karp(d: list) -> tuple[int, list, int]:
    """best[(set, last)] = shortest route from 0 visiting exactly that set of branches, ending at last (Figure 13.2).
    Sets are bit masks. Returns (round length, round, table entries)."""
    n = len(d)
    if n == 1:
        return 0, [0, 0], 0
    best, came = {}, {}
    for j in range(1, n):
        best[(1 << j, j)] = d[0][j]
    for size in range(2, n):
        for subset in itertools.combinations(range(1, n), size):
            mask = sum(1 << j for j in subset)
            for j in subset:
                prev = mask ^ (1 << j)
                best[(mask, j)], came[(mask, j)] = min((best[(prev, k)] + d[k][j], k) for k in subset if k != j)
    full = (1 << n) - 2
    length, last = min((best[(full, j)] + d[j][0], j) for j in range(1, n))
    route, mask = [0], full
    while last != 0:
        route.append(last)
        nxt = came.get((mask, last), 0)
        mask ^= 1 << last
        last = nxt
    route.append(0)
    return length, route[::-1], len(best)


def held_karp_masks(d: list) -> tuple[int, dict]:
    """The same table with explicit bit operations (Section 13.4): places 1..n-1 are bits 1..n-1 of a mask.
    Masks are visited in increasing numeric order, which puts every set after all of its subsets.
    Returns (round length, the table best[mask][j] as a dict of dicts)."""
    n = len(d)
    if n == 1:
        return 0, {}
    full = (1 << n) - 2                                # every place except home (bit 0)
    inf = float("inf")
    best = {}
    for mask in range(2, full + 1, 2):                 # even masks only: bit 0 (home) is never in a set
        row = {}
        for j in range(1, n):
            if not mask & (1 << j):                    # j must be in the set
                continue
            prev = mask & ~(1 << j)                    # the set without j: a smaller number
            if prev == 0:
                row[j] = d[0][j]
            else:
                row[j] = min((best[prev][k] + d[k][j] for k in range(1, n) if prev & (1 << k)), default=inf)
        best[mask] = row
    return min(best[full][j] + d[j][0] for j in range(1, n)), best


def brute(d: list) -> int:
    n = len(d)
    return min(sum(d[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, n))) if n > 1 else 0


if __name__ == "__main__":
    d = matrix(BRANCHES, TRAVEL)
    length, route, entries = held_karp(d)
    print(length, [BRANCHES[i] for i in route], entries, brute(d))
    for n in (5, 10, 15, 20):
        print(n, math.factorial(n - 1), (n - 1) * 2 ** (n - 1))
    r = random.Random(13)
    pts = [(r.random(), r.random()) for _ in range(12)]
    dd = [[round(100 * math.dist(p, q)) for q in pts] for p in pts]
    print(held_karp(dd)[0], held_karp(dd)[2])
