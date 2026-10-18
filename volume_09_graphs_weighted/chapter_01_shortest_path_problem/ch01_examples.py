"""Volume 9, Chapter 1 - The Shortest Path Problem: GPS Navigation.

A weighted graph is a dict: graph[u] = {v: weight of edge u -> v}.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import math
from collections import deque
from typing import Hashable

WGraph = dict[Hashable, dict[Hashable, float]]


def route_cost(graph: WGraph, route: list[Hashable]) -> float:
    """Total weight of a route; infinity if some step isn't a road."""
    return sum(graph.get(a, {}).get(b, math.inf) for a, b in zip(route, route[1:]))


def brute_force_shortest(graph: WGraph, source: Hashable, target: Hashable) -> tuple[float, list[Hashable] | None]:
    """Try every simple path (exponential!) - the obviously correct reference answer for tiny graphs."""
    best: tuple[float, list[Hashable] | None] = (math.inf, None)
    path = [source]

    def explore(v: Hashable, cost: float) -> None:
        nonlocal best
        if v == target:
            if cost < best[0]:
                best = (cost, list(path))
            return
        for w, wt in graph.get(v, {}).items():
            if w not in path:
                path.append(w)
                explore(w, cost + wt)
                path.pop()

    explore(source, 0.0)
    return best


def fewest_hops(graph: WGraph, source: Hashable, target: Hashable) -> list[Hashable] | None:
    """BFS ignores weights: fewest ROADS, not shortest DISTANCE (V8-C5)."""
    parent: dict[Hashable, Hashable | None] = {source: None}
    queue = deque([source])
    while queue:
        v = queue.popleft()
        if v == target:
            out = []
            while v is not None:
                out.append(v)
                v = parent[v]
            return out[::-1]
        for w in graph.get(v, {}):
            if w not in parent:
                parent[w] = v
                queue.append(w)
    return None


def relax(graph: WGraph, dist: dict[Hashable, float], parent: dict, u: Hashable, v: Hashable) -> bool:
    """THE core step of every shortest-path algorithm: if going through u gives v a shorter distance, take it."""
    if dist[u] + graph[u][v] < dist[v]:
        dist[v] = dist[u] + graph[u][v]
        parent[v] = u
        return True
    return False


def relax_until_stable(graph: WGraph, source: Hashable) -> dict[Hashable, float]:
    """Simplest correct method (if no negative cycles): relax every edge, over and over, until nothing improves.
    Chapters 2-4 show smarter ORDERS of relaxing that do far less work."""
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
    return dist


def delivery_eta(graph: WGraph, depot: Hashable, minutes_per_km: float) -> dict[Hashable, float]:
    """Industry example: estimated arrival time from a depot to every address."""
    return {v: round(d * minutes_per_km, 1) for v, d in relax_until_stable(graph, depot).items() if d < math.inf}


if __name__ == "__main__":
    city = {"Home": {"School": 4, "Park": 1}, "Park": {"School": 2, "Mall": 6}, "School": {"Mall": 1}, "Mall": {}}
    print("fewest roads:", fewest_hops(city, "Home", "Mall"), "cost", route_cost(city, fewest_hops(city, "Home", "Mall")))
    print("shortest:", brute_force_shortest(city, "Home", "Mall"))
    print("all distances:", relax_until_stable(city, "Home"))
    print("ETAs (min):", delivery_eta(city, "Home", 2.5))
