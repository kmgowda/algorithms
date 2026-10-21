"""Volume 6, Chapter 25 - Exact Algorithms for Hard Problems: smarter exponential searches.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

import bisect
import itertools
import random

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def cover_branching(edges: list, k: int, calls: list) -> list | None:
    """Vertex cover of size at most k (Figure 25.2): any uncovered road needs one of its two ends, so try each.
    At most 2^k branches, however many places there are."""
    calls[0] += 1
    if not edges:
        return []
    if k == 0:
        return None
    a, b = edges[0]
    for v in (a, b):
        rest = cover_branching([e for e in edges if v not in e], k - 1, calls)
        if rest is not None:
            return [v] + rest
    return None


def cover_brute(vertices: list, edges: list, k: int) -> tuple[list | None, int]:
    tried = 0
    for size in range(k + 1):
        for g in itertools.combinations(vertices, size):
            tried += 1
            if all(a in g or b in g for a, b in edges):
                return list(g), tried
    return None, tried


def subset_sum_mitm(values: list, target: int) -> tuple[bool, int]:
    """Meet in the middle (Figure 25.3): all sums of each half (2^(n/2) each), sort one, look up the other.
    Returns (found?, sums listed)."""
    half = len(values) // 2
    left, right = values[:half], values[half:]
    sums = lambda vs: [sum(c) for k in range(len(vs) + 1) for c in itertools.combinations(vs, k)]
    ls, rs = sums(left), sorted(sums(right))
    for s in ls:
        i = bisect.bisect_left(rs, target - s)
        if i < len(rs) and rs[i] == target - s:
            return True, len(ls) + len(rs)
    return False, len(ls) + len(rs)


if __name__ == "__main__":
    c = [0]
    print(cover_branching(ROADS, 4, c), c[0], cover_brute(TOWN, ROADS, 4))
    c = [0]
    print(cover_branching(ROADS, 3, c), c[0])
    r = random.Random(25)
    vals = [r.randint(1, 10 ** 6) for _ in range(24)]
    target = sum(vals[::3])
    print(subset_sum_mitm(vals, target), subset_sum_mitm(vals, 1), 2 ** 24)
