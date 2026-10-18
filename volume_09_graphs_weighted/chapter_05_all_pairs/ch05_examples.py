"""Volume 9, Chapter 5 - All-Pairs Shortest Paths: Floyd-Warshall and Johnson.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import heapq
import math

INF = math.inf


def floyd_warshall(n: int, edges: list[tuple[int, int, float]]) -> tuple[list[list[float]], list[list[int | None]]]:
    """dist[i][j] after step k = shortest i -> j using only intermediate vertices 0..k.
    Three nested loops, O(V^3). Handles negative edges; dist[i][i] < 0 afterwards means a negative cycle."""
    dist = [[0.0 if i == j else INF for j in range(n)] for i in range(n)]
    nxt: list[list[int | None]] = [[j if i == j else None for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v], nxt[u][v] = w, v
    for k in range(n):                                   # allow k as a stop-over
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def fw_path(nxt: list[list[int | None]], i: int, j: int) -> list[int]:
    """Rebuild a route from the 'next hop' table."""
    if nxt[i][j] is None:
        return []
    path = [i]
    while i != j:
        i = nxt[i][j]                                    # type: ignore[assignment]
        path.append(i)
    return path


def johnson(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]] | None:
    """Sparse graphs with negative edges: Bellman-Ford once to get potentials h, reweight
    w'(u, v) = w + h(u) - h(v) >= 0, then Dijkstra from every vertex. O(VE log V). None if a negative cycle exists."""
    h = [0.0] * n                                        # virtual source joined to all with weight 0
    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if h[u] + w < h[v]:
                h[v] = h[u] + w
                changed = True
        if not changed:
            break
    else:
        if any(h[u] + w < h[v] for u, v, w in edges):
            return None
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w + h[u] - h[v]))
    result = []
    for s in range(n):
        d = [INF] * n
        d[s] = 0.0
        heap = [(0.0, s)]
        while heap:
            du, u = heapq.heappop(heap)
            if du > d[u]:
                continue
            for v, w in adj[u]:
                if du + w < d[v]:
                    d[v] = du + w
                    heapq.heappush(heap, (d[v], v))
        result.append([d[v] - h[s] + h[v] if d[v] < INF else INF for v in range(n)])
    return result


def distance_table(cities: list[str], roads: list[tuple[str, str, float]]) -> dict[str, dict[str, float]]:
    """Industry example: the distance chart printed in road atlases - every city to every city."""
    idx = {c: i for i, c in enumerate(cities)}
    edges = [(idx[a], idx[b], w) for a, b, w in roads] + [(idx[b], idx[a], w) for a, b, w in roads]
    dist, _ = floyd_warshall(len(cities), edges)
    return {a: {b: dist[idx[a]][idx[b]] for b in cities} for a in cities}


def best_meeting_city(cities: list[str], roads: list[tuple[str, str, float]]) -> str:
    """Practical example: the city minimising the farthest anyone must travel (the graph's 'centre')."""
    table = distance_table(cities, roads)
    return min(cities, key=lambda c: (max(table[c].values()), c))


if __name__ == "__main__":
    edges = [(0, 1, 3), (1, 2, -2), (0, 2, 4), (2, 3, 2), (3, 0, 1)]
    dist, nxt = floyd_warshall(4, edges)
    print(dist, "| route 0->3:", fw_path(nxt, 0, 3))
    print("Johnson agrees:", johnson(4, edges) == dist)
    cities = ["Pune", "Mumbai", "Nashik", "Surat"]
    roads = [("Pune", "Mumbai", 150), ("Mumbai", "Nashik", 170), ("Pune", "Nashik", 210), ("Mumbai", "Surat", 280)]
    print(distance_table(cities, roads)["Pune"], "| meeting city:", best_meeting_city(cities, roads))
