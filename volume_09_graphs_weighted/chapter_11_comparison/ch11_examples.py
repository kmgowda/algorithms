"""Volume 9, Chapter 11 - The Big Comparison: Dijkstra vs. Bellman-Ford vs. Floyd-Warshall vs. A*; Kruskal vs. Prim.

Compact versions are repeated here so they can be raced in one file.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import heapq
import math
import random
import timeit


def random_road_grid(n: int, seed: int = 0) -> tuple[list[list[tuple[int, float]]], list[tuple[int, int, float]]]:
    """An n x n grid of junctions with random road lengths (1-9): adjacency list and edge list."""
    rng = random.Random(seed)
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n * n)]
    edges = []
    for r in range(n):
        for c in range(n):
            u = r * n + c
            for v in ((r + 1) * n + c if r + 1 < n else None, r * n + c + 1 if c + 1 < n else None):
                if v is not None:
                    w = rng.randint(1, 9)
                    adj[u].append((v, w))
                    adj[v].append((u, w))
                    edges += [(u, v, w), (v, u, w)]
    return adj, edges


def dijkstra(adj, s: int) -> list[float]:
    dist = [math.inf] * len(adj)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


def bellman_ford(n: int, edges, s: int) -> list[float]:
    dist = [math.inf] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return dist


def floyd_warshall(n: int, edges) -> list[list[float]]:
    d = [[0 if i == j else math.inf for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik, di = d[i][k], d[i]
            if dik == math.inf:
                continue
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return d


def a_star(adj, n: int, s: int, t: int) -> tuple[float, int]:
    """Grid A* with Manhattan distance (every road is at least 1 long, so it's admissible). Returns (cost, expanded)."""
    def h(x: int) -> int:
        return abs(x // n - t // n) + abs(x % n - t % n)
    g = {s: 0}
    heap = [(h(s), h(s), s)]
    done, expanded = set(), 0
    while heap:
        _, _, u = heapq.heappop(heap)
        if u in done:
            continue
        if u == t:
            return g[u], expanded
        done.add(u)
        expanded += 1
        for v, w in adj[u]:
            if g[u] + w < g.get(v, math.inf):
                g[v] = g[u] + w
                heapq.heappush(heap, (g[v] + h(v), h(v), v))
    return math.inf, expanded


def race_shortest(n: int) -> dict[str, float]:
    """Same grid, distances from one corner: Dijkstra vs. Bellman-Ford; and all pairs: Floyd-Warshall vs. V x Dijkstra."""
    adj, edges = random_road_grid(n)
    V = n * n
    one = {"Dijkstra": min(timeit.repeat(lambda: dijkstra(adj, 0), number=1, repeat=3)),
           "Bellman-Ford": min(timeit.repeat(lambda: bellman_ford(V, edges, 0), number=1, repeat=3))}
    allp = {"Floyd-Warshall (all pairs)": min(timeit.repeat(lambda: floyd_warshall(V, edges), number=1, repeat=1)),
            "Dijkstra from every vertex": min(timeit.repeat(lambda: [dijkstra(adj, s) for s in range(V)], number=1, repeat=1))}
    return one | allp


def choose(task: str) -> str:
    return {
        "one source, non-negative weights": "Dijkstra",
        "one source, negative edges or negative-cycle check": "Bellman-Ford",
        "one source, DAG": "DAG relaxation in topological order",
        "all pairs, small or dense graph": "Floyd-Warshall",
        "all pairs, sparse graph with negative edges": "Johnson",
        "one source and one target with a good estimate": "A*",
        "unweighted": "BFS",
        "cheapest network, sparse edge list": "Kruskal",
        "cheapest network, dense or complete graph": "Prim (array version)",
        "most throughput": "max flow (Edmonds-Karp)",
        "pairing people and jobs": "bipartite matching / assignment",
        "use every road once": "Hierholzer (Euler)",
    }[task]


if __name__ == "__main__":
    adj, edges = random_road_grid(25)
    d = dijkstra(adj, 0)
    print("Dijkstra == Bellman-Ford:", d == bellman_ford(625, edges, 0))
    cost, expanded = a_star(adj, 25, 0, 624)
    print(f"A* corner-to-corner cost {cost} == Dijkstra {d[624]}; expanded {expanded} of 625")
    print({k: round(v, 5) for k, v in race_shortest(12).items()})
    print(choose("one source, non-negative weights"))
