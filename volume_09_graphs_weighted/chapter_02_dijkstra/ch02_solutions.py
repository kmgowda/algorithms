"""Volume 9, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

import heapq
import math

from ch02_examples import WGraph, dijkstra


def cheapest_flight_cost(n: int, flights: list[tuple[int, int, int]], src: int, dst: int) -> float:
    """Exercise 1: cheapest total fare (no stop limit) - plain Dijkstra on fares."""
    graph: WGraph = {v: {} for v in range(n)}
    for a, b, price in flights:
        graph[a][b] = min(price, graph[a].get(b, math.inf))
    return dijkstra(graph, src)[0].get(dst, math.inf)


def min_effort_path(heights: list[list[int]]) -> int:
    """Exercise 2 (LeetCode 1631): a hiking route's 'effort' is its biggest single height step.
    Dijkstra still works when a path's cost is the MAX of its steps instead of the sum."""
    rows, cols = len(heights), len(heights[0])
    best = [[math.inf] * cols for _ in range(rows)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        effort, r, c = heapq.heappop(heap)
        if (r, c) == (rows - 1, cols - 1):
            return effort
        if effort > best[r][c]:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                e = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if e < best[nr][nc]:
                    best[nr][nc] = e
                    heapq.heappush(heap, (e, nr, nc))
    return 0


def most_reliable_path(graph: dict, source, target) -> float:
    """Exercise 3: each link succeeds with probability p; maximise the product.
    Using weights -log(p) turns 'maximise product' into 'minimise sum' - then Dijkstra applies."""
    logs: WGraph = {u: {v: -math.log(p) for v, p in nbrs.items()} for u, nbrs in graph.items()}
    d = dijkstra(logs, source)[0].get(target, math.inf)
    return math.exp(-d) if d < math.inf else 0.0


def settled_order(graph: WGraph, source) -> list:
    """Exercise 4: Dijkstra settles vertices in order of distance - list them."""
    dist, _ = dijkstra(graph, source)
    return sorted(dist, key=lambda v: (dist[v], str(v)))


if __name__ == "__main__":
    print(cheapest_flight_cost(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2))
    print(min_effort_path([[1, 2, 2], [3, 8, 2], [5, 3, 5]]))
    print(round(most_reliable_path({"a": {"b": 0.9, "c": 0.5}, "b": {"c": 0.9}, "c": {}}, "a", "c"), 2))
    print(settled_order({"a": {"b": 3, "c": 1}, "c": {"b": 1}, "b": {}}, "a"))
