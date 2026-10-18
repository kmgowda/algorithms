"""Volume 9, Chapter 4 - Shortest (and Longest) Paths in DAGs: Project Deadlines and Critical Paths.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import math
from collections import deque
from typing import Hashable

WGraph = dict[Hashable, dict[Hashable, float]]


def topological_order(graph: WGraph) -> list[Hashable]:
    """Kahn's algorithm (V8-C7). Raises if the graph has a cycle."""
    indeg: dict[Hashable, int] = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indeg[v] = indeg.get(v, 0) + 1
    ready = deque(v for v in indeg if indeg[v] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in graph.get(u, {}):
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    if len(order) != len(indeg):
        raise ValueError("graph has a cycle - not a DAG")
    return order


def dag_shortest(graph: WGraph, source: Hashable) -> dict[Hashable, float]:
    """Relax edges in topological order, each exactly once. Negative weights are fine (no cycles to exploit). O(V + E)."""
    order = topological_order(graph)
    dist = {v: math.inf for v in order}
    dist[source] = 0.0
    for u in order:
        if dist[u] == math.inf:
            continue
        for v, w in graph.get(u, {}).items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def dag_longest(graph: WGraph, source: Hashable) -> dict[Hashable, float]:
    """Longest paths are hard in general graphs, but easy in DAGs: same pass, with max instead of min."""
    order = topological_order(graph)
    dist = {v: -math.inf for v in order}
    dist[source] = 0.0
    for u in order:
        if dist[u] == -math.inf:
            continue
        for v, w in graph.get(u, {}).items():
            dist[v] = max(dist[v], dist[u] + w)
    return dist


def critical_path(tasks: dict[str, tuple[float, list[str]]]) -> tuple[float, list[str]]:
    """Industry example: project scheduling. tasks[name] = (duration, prerequisites).
    The project can't finish before the LONGEST chain of dependent tasks - the critical path."""
    graph: WGraph = {t: {} for t in tasks}
    for t, (_, prereqs) in tasks.items():
        for p in prereqs:
            graph[p][t] = tasks[p][0]                # finishing p takes p's duration before t may start
    finish: dict[str, float] = {}
    best_prev: dict[str, str | None] = {}
    for t in topological_order(graph):
        start, prev = 0.0, None
        for p in tasks[t][1]:
            if finish[p] > start:
                start, prev = finish[p], p
        finish[t] = start + tasks[t][0]
        best_prev[t] = prev
    end = max(finish, key=lambda t: finish[t])
    chain, v = [], end
    while v is not None:
        chain.append(v)
        v = best_prev[v]
    return finish[end], chain[::-1]


if __name__ == "__main__":
    g = {"s": {"a": 3, "b": 1}, "a": {"c": -2}, "b": {"a": 1, "c": 5}, "c": {"t": 2}, "t": {}}
    print("shortest:", dag_shortest(g, "s"), "| longest:", dag_longest(g, "s"))
    house = {"foundation": (5, []), "walls": (7, ["foundation"]), "plumbing": (3, ["foundation"]),
             "roof": (4, ["walls"]), "electrics": (2, ["walls", "plumbing"]), "paint": (3, ["roof", "electrics"])}
    print("critical path:", critical_path(house))
