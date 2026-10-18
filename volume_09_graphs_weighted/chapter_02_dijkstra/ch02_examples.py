"""Volume 9, Chapter 2 - Dijkstra's Algorithm.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import heapq
import itertools
import math
from typing import Hashable

WGraph = dict[Hashable, dict[Hashable, float]]


def dijkstra(graph: WGraph, source: Hashable) -> tuple[dict[Hashable, float], dict[Hashable, Hashable | None]]:
    """Non-negative weights only. Repeatedly SETTLE the unsettled vertex with the smallest distance, then relax its
    edges. A heap gives the next-closest vertex fast; stale heap entries are skipped ('lazy deletion'). O(E log V)."""
    dist: dict[Hashable, float] = {source: 0.0}
    parent: dict[Hashable, Hashable | None] = {source: None}
    settled: set[Hashable] = set()
    tie = itertools.count()                       # avoids comparing vertices when distances tie
    heap = [(0.0, next(tie), source)]
    while heap:
        d, _, u = heapq.heappop(heap)
        if u in settled:
            continue                              # an outdated entry - u was already settled with a smaller d
        settled.add(u)
        for v, w in graph.get(u, {}).items():
            if w < 0:
                raise ValueError("Dijkstra needs non-negative weights")
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v], parent[v] = nd, u
                heapq.heappush(heap, (nd, next(tie), v))
    return dist, parent


def route(parent: dict[Hashable, Hashable | None], target: Hashable) -> list[Hashable]:
    out: list[Hashable] = []
    v: Hashable | None = target
    while v is not None:
        out.append(v)
        v = parent[v]
    return out[::-1]


def dijkstra_to_target(graph: WGraph, source: Hashable, target: Hashable) -> tuple[float, list[Hashable]]:
    """Early exit: once the target is settled, its distance is final - stop."""
    dist: dict[Hashable, float] = {source: 0.0}
    parent: dict[Hashable, Hashable | None] = {source: None}
    settled: set[Hashable] = set()
    tie = itertools.count()
    heap = [(0.0, next(tie), source)]
    while heap:
        d, _, u = heapq.heappop(heap)
        if u in settled:
            continue
        if u == target:
            return d, route(parent, target)
        settled.add(u)
        for v, w in graph.get(u, {}).items():
            if d + w < dist.get(v, math.inf):
                dist[v], parent[v] = d + w, u
                heapq.heappush(heap, (d + w, next(tie), v))
    return math.inf, []


def network_delay(times: list[tuple[int, int, int]], n: int, start: int) -> int:
    """Industry example (LeetCode 743): a signal sent from one server - when has every server received it?"""
    graph: WGraph = {v: {} for v in range(1, n + 1)}
    for u, v, w in times:
        graph[u][v] = w
    dist, _ = dijkstra(graph, start)
    return int(max(dist.values())) if len(dist) == n else -1


def counterexample_negative() -> tuple[float, float]:
    """Why negative edges break Dijkstra: B gets settled at 2 before the cheaper path A->C->B (5 - 4 = 1) is seen."""
    g = {"A": {"B": 2, "C": 5}, "C": {"B": -4}, "B": {}}
    dist: dict[Hashable, float] = {"A": 0.0}
    settled: set[Hashable] = set()
    heap = [(0.0, "A")]
    while heap:                                   # Dijkstra without the safety check
        d, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        for v, w in g[u].items():
            if v not in settled and d + w < dist.get(v, math.inf):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist["B"], 1.0                         # (what Dijkstra reports, the truth)


if __name__ == "__main__":
    city = {"Depot": {"Market": 7, "School": 9, "Park": 14}, "Market": {"School": 10, "Mill": 15},
            "School": {"Mill": 11, "Park": 2}, "Park": {"Lake": 9}, "Mill": {"Lake": 6}, "Lake": {}}
    dist, parent = dijkstra(city, "Depot")
    print(dist)
    print("route to Lake:", route(parent, "Lake"), "| early exit:", dijkstra_to_target(city, "Depot", "Mill"))
    print("network delay:", network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2))
    print("negative edge: Dijkstra says", counterexample_negative())
