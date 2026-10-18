"""Volume 9, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

import math
from collections import deque
from typing import Hashable

from ch03_examples import Edge, bellman_ford


def rounds_needed(vertices: list[Hashable], edges: list[Edge], source: Hashable) -> int:
    """Exercise 1: how many rounds until nothing changes (at most V - 1 without negative cycles)?"""
    dist = {v: math.inf for v in vertices}
    dist[source] = 0.0
    for r in range(1, len(vertices) + 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            return r - 1
    return len(vertices)


def spfa(vertices: list[Hashable], edges: list[Edge], source: Hashable) -> dict[Hashable, float]:
    """Exercise 2: the 'queue-based Bellman-Ford' - only relax edges out of vertices whose distance just changed.
    Often much faster in practice; same worst case. (Assumes no negative cycle.)"""
    out: dict[Hashable, list[tuple[Hashable, float]]] = {v: [] for v in vertices}
    for u, v, w in edges:
        out[u].append((v, w))
    dist = {v: math.inf for v in vertices}
    dist[source] = 0.0
    queue, in_queue = deque([source]), {source}
    while queue:
        u = queue.popleft()
        in_queue.discard(u)
        for v, w in out[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if v not in in_queue:
                    queue.append(v)
                    in_queue.add(v)
    return dist


def affected_by_negative_cycle(vertices: list[Hashable], edges: list[Edge], source: Hashable) -> set[Hashable]:
    """Exercise 3: vertices whose 'shortest distance' is minus infinity (reachable from a reachable negative cycle)."""
    dist, _, _ = bellman_ford(vertices, edges, source)
    bad = {v for u, v, w in edges if dist[u] + w < dist[v]}
    out: dict[Hashable, list[Hashable]] = {v: [] for v in vertices}
    for u, v, _ in edges:
        out[u].append(v)
    stack = list(bad)
    while stack:
        x = stack.pop()
        for y in out[x]:
            if y not in bad:
                bad.add(y)
                stack.append(y)
    return bad


if __name__ == "__main__":
    V = ["A", "B", "C", "D"]
    E = [("A", "B", 4), ("A", "C", 5), ("C", "B", -3), ("B", "D", 2)]
    print(rounds_needed(V, E, "A"), spfa(V, E, "A"))
    print(affected_by_negative_cycle(["s", "a", "b", "t"], [("s", "a", 1), ("a", "b", -2), ("b", "a", 1), ("b", "t", 1)], "s"))
