"""Volume 9, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

import math
from typing import Hashable

from ch01_examples import WGraph, relax


def path_from_parents(parent: dict, target: Hashable) -> list[Hashable]:
    """Exercise 1: walk parent pointers back from the target."""
    out = []
    v: Hashable | None = target
    while v is not None:
        out.append(v)
        v = parent.get(v)
    return out[::-1]


def shortest_with_route(graph: WGraph, source: Hashable, target: Hashable) -> tuple[float, list[Hashable]]:
    """Exercise 2: relax until stable, keeping parents, then rebuild the route."""
    vertices = set(graph) | {w for u in graph for w in graph[u]}
    dist = {v: math.inf for v in vertices}
    parent: dict = {source: None}
    dist[source] = 0.0
    changed = True
    while changed:
        changed = False
        for u in graph:
            if dist[u] < math.inf:
                for v in graph[u]:
                    changed |= relax(graph, dist, parent, u, v)
    return dist[target], path_from_parents(parent, target) if dist[target] < math.inf else []


def count_relaxations(graph: WGraph, source: Hashable) -> int:
    """Exercise 3: how many successful relaxations does the naive method make?"""
    vertices = set(graph) | {w for u in graph for w in graph[u]}
    dist = {v: math.inf for v in vertices}
    parent: dict = {source: None}
    dist[source] = 0.0
    count, changed = 0, True
    while changed:
        changed = False
        for u in graph:
            if dist[u] < math.inf:
                for v in graph[u]:
                    if relax(graph, dist, parent, u, v):
                        count += 1
                        changed = True
    return count


def make_two_way(roads: list[tuple[str, str, float]]) -> WGraph:
    """Exercise 4: two-way roads become two directed edges with the same weight."""
    g: WGraph = {}
    for a, b, w in roads:
        g.setdefault(a, {})[b] = w
        g.setdefault(b, {})[a] = w
    return g


if __name__ == "__main__":
    city = {"Home": {"School": 4, "Park": 1}, "Park": {"School": 2, "Mall": 6}, "School": {"Mall": 1}, "Mall": {}}
    print(shortest_with_route(city, "Home", "Mall"), count_relaxations(city, "Home"))
    print(make_two_way([("A", "B", 3)]))
