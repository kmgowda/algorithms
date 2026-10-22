"""Volume 7, Chapter 27 - Local Search and Simulated Annealing: improve a round by small changes.

Run:  python3 ch27_examples.py
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
    """Reverse a stretch of the round whenever that shortens it, until no reversal helps (Figure 27.2).
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
    """Like 2-opt, but sometimes accept a longer round, less often as the 'temperature' cools (Figure 27.3)."""
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
    """Held-Karp (Volume 6, Chapter 21) for checking."""
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


def two_opt_delta(tour: list, pts: list, i: int, j: int) -> float:
    """Change in length when tour[i..j] is reversed: only the two roads at the ends of the stretch change."""
    n = len(tour)
    a, b = pts[tour[i - 1]], pts[tour[i]]
    c, d = pts[tour[j]], pts[tour[(j + 1) % n]]
    return math.dist(a, c) + math.dist(b, d) - math.dist(a, b) - math.dist(c, d)


def restarts(pts: list, runs: int, seed: int) -> tuple[float, int]:
    """Random-restart 2-opt: run from several random rounds and keep the best. Returns (best length, runs that hit it)."""
    results = [round(length(two_opt(random.Random(seed + s).sample(range(len(pts)), len(pts)), pts)[0], pts), 1)
               for s in range(runs)]
    best = min(results)
    return best, results.count(best)


TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def cut_size(side: dict, edges: list) -> int:
    return sum(1 for a, b in edges if side[a] != side[b])


def max_cut_local(vertices: list, edges: list, start: dict | None = None) -> tuple[dict, int, int]:
    """Local search for a maximum cut (Figure 27.4): move one place to the other side whenever that increases the
    number of roads crossing between the sides. Ends with at least half of all roads crossing.
    Returns (sides, cut size, moves)."""
    side = dict(start) if start else {v: 0 for v in vertices}
    moves, improved = 0, True
    while improved:
        improved = False
        for v in vertices:
            same = sum(1 for a, b in edges if v in (a, b) and side[a] == side[b])
            other = sum(1 for a, b in edges if v in (a, b) and side[a] != side[b])
            if same > other:
                side[v] = 1 - side[v]
                moves += 1
                improved = True
    return side, cut_size(side, edges), moves


def max_cut_brute(vertices: list, edges: list) -> int:
    best = 0
    for bits in itertools.product([0, 1], repeat=len(vertices) - 1):
        side = dict(zip(vertices, (0,) + bits))
        best = max(best, cut_size(side, edges))
    return best


def min_conflicts_colouring(vertices: list, edges: list, k: int, rng, steps: int = 1000) -> tuple[dict | None, int]:
    """Local search for a timetable (colouring): start anywhere, repeatedly pick a clashing place and give it the
    colour with fewest clashes. Returns (colouring or None, steps used)."""
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    col = {v: rng.randrange(k) for v in vertices}
    for step in range(steps):
        clashing = [v for v in vertices if any(col[u] == col[v] for u in adj[v])]
        if not clashing:
            return col, step
        v = rng.choice(clashing)
        col[v] = min(range(k), key=lambda c: (sum(1 for u in adj[v] if col[u] == c), rng.random()))
    return None, steps


if __name__ == "__main__":
    pts = places(12, 1)
    start = list(range(12))
    rng = random.Random(24)
    t2, moves = two_opt(start, pts)
    ta = annealing(start, pts, rng)
    print(round(length(start, pts), 1), round(length(t2, pts), 1), moves, round(length(ta, pts), 1), round(exact(pts), 1))
    stuck = [round(length(two_opt(random.Random(s).sample(range(12), 12), pts)[0], pts), 1) for s in range(10)]
    print(stuck)
    print(restarts(pts, 20, 100), round(two_opt_delta(start, pts, 2, 7), 3),
          round(length(start[:2] + start[2:8][::-1] + start[8:], pts) - length(start, pts), 3))
    side, cut, mv = max_cut_local(TOWN, ROADS)
    print(sorted(v for v in TOWN if side[v]), cut, mv, max_cut_brute(TOWN, ROADS), len(ROADS) / 2)
    print(min_conflicts_colouring(TOWN, ROADS, 3, random.Random(5)))
