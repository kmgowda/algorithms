"""Volume 15, Chapter 4 - Approximation Algorithms: Vertex Cover, Set Cover, TSP.

An approximation algorithm runs in polynomial time and PROVABLY stays within a factor of the optimum.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import itertools
import math
import random

Point = tuple[float, float]


def vertex_cover_2approx(edges: list[tuple[int, int]]) -> set[int]:
    """Take any uncovered edge and add BOTH ends. The chosen edges share no vertex, and any cover needs one end
    of each, so the result is at most 2 x OPT."""
    cover: set[int] = set()
    for u, v in edges:
        if u not in cover and v not in cover:
            cover |= {u, v}
    return cover


def vertex_cover_exact(edges: list[tuple[int, int]]) -> int:
    """Brute force: the smallest cover size (for checking ratios on small graphs)."""
    nodes = sorted({x for e in edges for x in e})
    for r in range(len(nodes) + 1):
        for s in itertools.combinations(nodes, r):
            chosen = set(s)
            if all(u in chosen or v in chosen for u, v in edges):
                return r
    return 0


def greedy_set_cover(universe: set[int], subsets: dict[str, set[int]]) -> list[str]:
    """Repeatedly pick the subset covering the most still-uncovered items. Within a factor ln(n) + 1 of optimal -
    and no polynomial algorithm can do much better unless P = NP."""
    uncovered, chosen = set(universe), []
    while uncovered:
        best = max(subsets, key=lambda name: len(subsets[name] & uncovered))
        if not subsets[best] & uncovered:
            raise ValueError("the subsets do not cover the universe")
        chosen.append(best)
        uncovered -= subsets[best]
    return chosen


def set_cover_exact(universe: set[int], subsets: dict[str, set[int]]) -> int:
    names = list(subsets)
    for r in range(len(names) + 1):
        for combo in itertools.combinations(names, r):
            if set().union(*(subsets[n] for n in combo)) >= universe:
                return r
    return -1


def tsp_mst_2approx(points: list[Point]) -> tuple[float, list[int]]:
    """Metric TSP: build a minimum spanning tree (Prim, V9-C7), walk it in preorder, skip repeated cities.
    Tour <= 2 x MST <= 2 x OPT (the triangle inequality makes shortcuts no longer)."""
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
            d = math.dist(points[u], points[v])
            if not in_tree[v] and d < best[v]:
                best[v], parent[v] = d, u
    order, stack = [], [0]
    while stack:
        u = stack.pop()
        order.append(u)
        stack.extend(reversed(children[u]))
    tour = order + [0]
    return sum(math.dist(points[a], points[b]) for a, b in zip(tour, tour[1:])), tour


def tsp_exact(points: list[Point]) -> float:
    n = len(points)
    if n <= 1:
        return 0.0
    return min(sum(math.dist(points[a], points[b]) for a, b in zip((0,) + p, p + (0,)))
               for p in itertools.permutations(range(1, n)))


def measured_ratios(trials: int, rng: random.Random) -> dict[str, float]:
    """Worst ratio (approx / optimal) seen on random small instances."""
    worst = {"vertex cover": 1.0, "set cover": 1.0, "TSP": 1.0}
    for _ in range(trials):
        edges = [(u, v) for u, v in itertools.combinations(range(7), 2) if rng.random() < 0.4]
        if edges:
            worst["vertex cover"] = max(worst["vertex cover"], len(vertex_cover_2approx(edges)) / vertex_cover_exact(edges))
        universe = set(range(10))
        subsets = {f"s{i}": set(rng.sample(range(10), rng.randint(1, 5))) for i in range(8)}
        subsets["all"] = set(range(10)) if rng.random() < 0.2 else set(range(5))
        subsets["rest"] = set(range(5, 10))
        worst["set cover"] = max(worst["set cover"], len(greedy_set_cover(universe, subsets)) / set_cover_exact(universe, subsets))
        pts = [(rng.random() * 100, rng.random() * 100) for _ in range(7)]
        worst["TSP"] = max(worst["TSP"], tsp_mst_2approx(pts)[0] / tsp_exact(pts))
    return worst


def place_cell_towers(villages: set[int], tower_sites: dict[str, set[int]]) -> list[str]:
    """Industry example: choose few tower sites so every village gets coverage (set cover)."""
    return greedy_set_cover(villages, tower_sites)


if __name__ == "__main__":
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    print("star cover:", vertex_cover_2approx(edges), "optimal size", vertex_cover_exact(edges))
    print(greedy_set_cover(set(range(1, 6)), {"A": {1, 2, 3}, "B": {2, 4}, "C": {3, 4}, "D": {4, 5}}))
    pts = [(0, 0), (0, 3), (4, 3), (4, 0), (2, 1)]
    print("TSP approx:", tsp_mst_2approx(pts), "optimal", round(tsp_exact(pts), 3))
    print("worst measured ratios:", {k: round(v, 3) for k, v in measured_ratios(60, random.Random(1)).items()})
    print(place_cell_towers(set(range(8)), {"hill": {0, 1, 2, 3}, "river": {3, 4, 5}, "farm": {5, 6, 7}, "school": {1, 6}}))
