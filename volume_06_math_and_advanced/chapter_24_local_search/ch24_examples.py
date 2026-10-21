"""Volume 6, Chapter 24 - Local Search and Simulated Annealing: improve a round by small changes.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

import itertools
import math
import random


def places(n: int, seed: int) -> list:
    r = random.Random(seed)
    return [(r.randint(0, 100), r.randint(0, 100)) for _ in range(n)]


def length(tour: list, pts: list) -> float:
    return sum(math.dist(pts[tour[i]], pts[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))


def two_opt(tour: list, pts: list) -> tuple[list, int]:
    """Reverse a stretch of the round whenever that shortens it, until no reversal helps (Figure 24.2).
    Returns (round, improvements made)."""
    tour, moves, better = list(tour), 0, True
    while better:
        better = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                new = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
                if length(new, pts) < length(tour, pts) - 1e-9:
                    tour, moves, better = new, moves + 1, True
    return tour, moves


def annealing(tour: list, pts: list, rng, steps: int = 20000, start_temp: float = 50.0) -> list:
    """Like 2-opt, but sometimes accept a longer round, less often as the 'temperature' cools (Figure 24.3)."""
    tour = list(tour)
    best = list(tour)
    for s in range(steps):
        temp = start_temp * (1 - s / steps) + 1e-9
        i, j = sorted(rng.sample(range(1, len(tour)), 2))
        new = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
        change = length(new, pts) - length(tour, pts)
        if change < 0 or rng.random() < math.exp(-change / temp):
            tour = new
            if length(tour, pts) < length(best, pts):
                best = list(tour)
    return best


def exact(pts: list) -> float:
    """Held-Karp (Volume 5, Chapter 13) for checking."""
    n = len(pts)
    d = [[math.dist(a, b) for b in pts] for a in pts]
    best = {(1 << j, j): d[0][j] for j in range(1, n)}
    for size in range(2, n):
        for sub in itertools.combinations(range(1, n), size):
            mask = sum(1 << j for j in sub)
            for j in sub:
                best[(mask, j)] = min(best[(mask ^ (1 << j), k)] + d[k][j] for k in sub if k != j)
    full = (1 << n) - 2
    return min(best[(full, j)] + d[j][0] for j in range(1, n))


if __name__ == "__main__":
    pts = places(12, 1)
    start = list(range(12))
    rng = random.Random(24)
    t2, moves = two_opt(start, pts)
    ta = annealing(start, pts, rng)
    print(round(length(start, pts), 1), round(length(t2, pts), 1), moves, round(length(ta, pts), 1), round(exact(pts), 1))
    stuck = [round(length(two_opt(random.Random(s).sample(range(12), 12), pts)[0], pts), 1) for s in range(10)]
    print(stuck)
