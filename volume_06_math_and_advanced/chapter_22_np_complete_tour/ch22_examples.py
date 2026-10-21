"""Volume 6, Chapter 22 - A Tour of NP-Complete Problems: five famous problems, each with a checker and a brute-force search.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

import itertools

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def satisfiable(clauses: list, n_vars: int) -> tuple[dict | None, int]:
    """Satisfiability: clauses are lists of +v / -v; try every true/false setting (Figure 22.1)."""
    tried = 0
    for bits in itertools.product([False, True], repeat=n_vars):
        tried += 1
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            return {v + 1: bits[v] for v in range(n_vars)}, tried
    return None, tried


def colouring(vertices: list, edges: list, k: int) -> tuple[dict | None, int]:
    tried = 0
    for cols in itertools.product(range(k), repeat=len(vertices)):
        tried += 1
        c = dict(zip(vertices, cols))
        if all(c[a] != c[b] for a, b in edges):
            return c, tried
    return None, tried


def vertex_cover(vertices: list, edges: list, k: int) -> list | None:
    for group in itertools.combinations(vertices, k):
        if all(a in group or b in group for a, b in edges):
            return list(group)
    return None


def bin_packing(sizes: list, capacity: int, bins: int) -> list | None:
    """Can the boxes fit in this many bins? Try every assignment."""
    for assign in itertools.product(range(bins), repeat=len(sizes)):
        load = [0] * bins
        for s, b in zip(sizes, assign):
            load[b] += s
        if max(load, default=0) <= capacity:
            return list(assign)
    return None


if __name__ == "__main__":
    clauses = [[1, 2], [-1, 3], [-2, -3], [2, 3]]
    print(satisfiable(clauses, 3), satisfiable([[1], [-1]], 1))
    print(colouring(TOWN, ROADS, 2)[0], colouring(TOWN, ROADS, 2)[1], colouring(TOWN, ROADS, 3))
    print(vertex_cover(TOWN, ROADS, 3), vertex_cover(TOWN, ROADS, 4), vertex_cover(TOWN, ROADS, 5))
    print(bin_packing([5, 4, 4, 3, 2, 2], 10, 2), bin_packing([6, 6, 6], 10, 2))
