"""Volume 15, Chapter 11 - The Big Comparison: Exact vs. Approximate vs. Randomized vs. Heuristic.

One problem - the shortest delivery round (TSP on points in the plane) - solved four ways.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import itertools
import math
import random
import time

Point = tuple[float, float]


def tour_length(points: list[Point], tour: list[int]) -> float:
    return sum(math.dist(points[tour[i - 1]], points[tour[i]]) for i in range(len(tour)))


def exact_tsp(points: list[Point]) -> list[int]:
    """EXACT: try every order with city 0 first - (n-1)! tours."""
    n = len(points)
    best = min(itertools.permutations(range(1, n)), key=lambda p: tour_length(points, [0, *p]))
    return [0, *best]


def mst_tour(points: list[Point]) -> list[int]:
    """APPROXIMATE (guaranteed <= 2 x optimal): preorder walk of a minimum spanning tree (Chapter 4)."""
    n = len(points)
    in_tree, parent, best = [False] * n, [-1] * n, [math.inf] * n
    best[0] = 0.0
    children: dict[int, list[int]] = {i: [] for i in range(n)}
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=lambda i: best[i])
        in_tree[u] = True
        if parent[u] >= 0:
            children[parent[u]].append(u)
        for v in range(n):
            if not in_tree[v] and math.dist(points[u], points[v]) < best[v]:
                best[v], parent[v] = math.dist(points[u], points[v]), u
    order, stack = [], [0]
    while stack:
        u = stack.pop()
        order.append(u)
        stack.extend(reversed(children[u]))
    return order


def nearest_neighbour(points: list[Point], start: int = 0) -> list[int]:
    """HEURISTIC: always drive to the closest unvisited stop. Fast and often decent - no guarantee."""
    tour, left = [start], set(range(len(points))) - {start}
    while left:
        nxt = min(left, key=lambda j: math.dist(points[tour[-1]], points[j]))
        tour.append(nxt)
        left.remove(nxt)
    return tour


def two_opt(points: list[Point], tour: list[int]) -> list[int]:
    """HEURISTIC local search: reverse any segment that shortens the tour, until no reversal helps."""
    tour = list(tour)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                a, b = points[tour[i - 1]], points[tour[i]]
                c, d = points[tour[j]], points[tour[(j + 1) % len(tour)]]
                if math.dist(a, c) + math.dist(b, d) < math.dist(a, b) + math.dist(c, d) - 1e-12:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
    return tour


def randomized_restarts(points: list[Point], restarts: int, rng: random.Random) -> list[int]:
    """RANDOMIZED: 2-opt from several random starting tours; keep the best (Chapter 1's amplification)."""
    best: list[int] | None = None
    for _ in range(restarts):
        start = list(range(len(points)))
        rng.shuffle(start)
        t = two_opt(points, start)
        if best is None or tour_length(points, t) < tour_length(points, best):
            best = t
    return best                                              # type: ignore[return-value]


def compare(n: int, seed: int) -> dict[str, tuple[float, float]]:
    """(tour length, seconds) for each approach on the same random cities."""
    rng = random.Random(seed)
    pts = [(rng.random() * 100, rng.random() * 100) for _ in range(n)]
    methods = {
        "exact": lambda: exact_tsp(pts) if n <= 9 else None,
        "MST 2-approximation": lambda: mst_tour(pts),
        "nearest neighbour": lambda: nearest_neighbour(pts),
        "nearest neighbour + 2-opt": lambda: two_opt(pts, nearest_neighbour(pts)),
        "random restarts + 2-opt": lambda: randomized_restarts(pts, 10, random.Random(seed)),
    }
    out = {}
    for name, fn in methods.items():
        start = time.perf_counter()
        tour = fn()
        if tour is not None:
            out[name] = (tour_length(pts, tour), time.perf_counter() - start)
    return out


def choose_approach(features: set[str]) -> str:
    """Decision guide for hard problems."""
    if "small input" in features:
        return "exact (brute force, backtracking, DP, branch-and-bound)"
    if "need a proven quality bound" in features:
        return "approximation algorithm"
    if "need good answers fast, no proof needed" in features:
        return "heuristic with local search and random restarts"
    if "huge data or tight time" in features:
        return "streaming, sampling, or simple greedy heuristic"
    return "start exact on small cases, then measure approximations and heuristics against it"


if __name__ == "__main__":
    for n in (9, 60):
        print(f"{n} cities:")
        for name, (length, secs) in compare(n, 1).items():
            print(f"   {name:<26} length {length:7.1f}   {secs * 1000:8.1f} ms")
