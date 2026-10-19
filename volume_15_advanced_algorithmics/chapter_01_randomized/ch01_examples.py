"""Volume 15, Chapter 1 - Randomized Algorithms: Las Vegas vs. Monte Carlo.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import random


def quickselect(values: list[int], k: int, rng: random.Random) -> tuple[int, int]:
    """LAS VEGAS: always correct, running time is random. k-th smallest (0-based) with a random pivot (V5-C10).
    Returns (answer, comparisons) - expected O(n) whatever the input order."""
    items, comparisons = list(values), 0
    while True:
        pivot = rng.choice(items)
        comparisons += len(items)
        less = [x for x in items if x < pivot]
        equal = [x for x in items if x == pivot]
        if k < len(less):
            items = less
        elif k < len(less) + len(equal):
            return pivot, comparisons
        else:
            k -= len(less) + len(equal)
            items = [x for x in items if x > pivot]


def freivalds(a: list[list[int]], b: list[list[int]], c: list[list[int]], rounds: int, rng: random.Random) -> bool:
    """MONTE CARLO: always fast, answer may be wrong with small probability. Does A x B equal C?
    Multiply by a random 0/1 vector r: compare A(Br) with Cr in O(n^2) instead of computing A x B in O(n^3).
    If A x B != C, one round catches it with probability >= 1/2; after `rounds` rounds the error is <= 2^-rounds."""
    n = len(a)
    for _ in range(rounds):
        r = [rng.randint(0, 1) for _ in range(n)]
        br = [sum(b[i][j] * r[j] for j in range(n)) for i in range(n)]
        abr = [sum(a[i][j] * br[j] for j in range(n)) for i in range(n)]
        cr = [sum(c[i][j] * r[j] for j in range(n)) for i in range(n)]
        if abr != cr:
            return False                                 # certainly different
    return True                                          # probably equal


def karger_cut(edges: list[tuple[int, int]], n: int, rng: random.Random) -> int:
    """MONTE CARLO: contract random edges until two super-vertices remain; the edges between them form a cut.
    One run finds a minimum cut with probability >= 2 / (n(n-1)); repeating raises the chance."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    order = edges[:]
    rng.shuffle(order)                                   # contracting in random order = random edge each time
    for u, v in order:
        if groups == 2:
            break
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            groups -= 1
    return sum(1 for u, v in edges if find(u) != find(v))


def min_cut_repeated(edges: list[tuple[int, int]], n: int, trials: int, rng: random.Random) -> int:
    return min(karger_cut(edges, n, rng) for _ in range(trials))


def load_balance(requests: int, servers: int, rng: random.Random, choices: int = 1) -> int:
    """Industry example: send each request to a random server (or the least loaded of `choices` random ones).
    Returns the busiest server's load. 'Power of two choices' dramatically flattens the peak."""
    load = [0] * servers
    for _ in range(requests):
        picks = [rng.randrange(servers) for _ in range(choices)]
        best = min(picks, key=lambda s: load[s])
        load[best] += 1
    return max(load)


if __name__ == "__main__":
    rng = random.Random(1)
    data = list(range(100000, 0, -1))
    print("quickselect median:", quickselect(data, 50000, rng))
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    print(freivalds(a, b, [[19, 22], [43, 50]], 20, rng), freivalds(a, b, [[19, 22], [43, 51]], 20, rng))
    cycle_pair = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4)]
    print("one Karger run:", karger_cut(cycle_pair, 8, rng), "| best of 50:", min_cut_repeated(cycle_pair, 8, 50, rng))
    print("max load, 1 choice:", load_balance(100000, 1000, rng), "| 2 choices:", load_balance(100000, 1000, rng, 2))
