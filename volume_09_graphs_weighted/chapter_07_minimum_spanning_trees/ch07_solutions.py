"""Volume 9, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

import itertools
from typing import Hashable

from ch07_examples import DSU, Edge, kruskal


def brute_force_mst(vertices: list[Hashable], edges: list[Edge]) -> float:
    """Exercise 1: try every set of V - 1 edges; keep the cheapest that connects everything (tiny graphs only)."""
    best = float("inf")
    for combo in itertools.combinations(edges, len(vertices) - 1):
        dsu = DSU(vertices)
        if all(dsu.union(u, v) for _, u, v in combo):
            best = min(best, sum(w for w, _, _ in combo))
    return best if len(vertices) > 1 else 0.0


def maximum_spanning_tree(vertices: list[Hashable], edges: list[Edge]) -> float:
    """Exercise 2: the most valuable tree (e.g. strongest links) - Kruskal on negated weights."""
    total, _ = kruskal(vertices, [(-w, u, v) for w, u, v in edges])
    return -total


def min_cost_with_wells(n: int, wells: list[int], pipes: list[tuple[int, int, int]]) -> int:
    """Exercise 3 (LeetCode 1168): each house can dig its own well or pipe from a neighbour.
    Trick: a virtual 'water source' vertex 0 connected to house i with weight wells[i-1]; then MST."""
    edges: list[Edge] = [(wells[i - 1], 0, i) for i in range(1, n + 1)] + [(c, a, b) for a, b, c in pipes]
    total, _ = kruskal(list(range(n + 1)), edges)
    return int(total)


def is_unique_mst(vertices: list[Hashable], edges: list[Edge]) -> bool:
    """Exercise 4: with all-distinct weights the MST is unique; check by trying each MST edge's removal."""
    best, chosen = kruskal(vertices, edges)
    for e in chosen:
        rest = [x for x in edges if x != e]
        total, tree = kruskal(vertices, rest)
        if len(tree) == len(vertices) - 1 and total == best:
            return False
    return True


if __name__ == "__main__":
    towns = ["A", "B", "C", "D", "E"]
    cables = [(4, "A", "B"), (1, "A", "C"), (3, "B", "C"), (2, "B", "D"), (5, "C", "D"), (7, "D", "E"), (6, "C", "E")]
    print(brute_force_mst(towns, cables), maximum_spanning_tree(towns, cables),
          min_cost_with_wells(3, [1, 2, 2], [(1, 2, 1), (2, 3, 1)]), is_unique_mst(towns, cables))
