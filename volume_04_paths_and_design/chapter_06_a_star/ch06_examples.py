"""Volume 4, Chapter 6 - A* Search: Dijkstra with a sense of direction.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import heapq
import math

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]
POS = {"Library": (0.55, 1.55), "School": (1.55, 2.45), "Park": (1.5, 0.85), "Market": (2.75, 1.6),
       "Station": (3.95, 2.45), "Museum": (3.9, 0.9), "Hospital": (2.7, 0.38), "Harbour": (5.0, 1.55)}


def weighted_adjacency(places=PLACES, roads=ROADS) -> dict:
    adj = {p: {} for p in places}
    for a, b, w in roads:
        adj[a][b] = w
        adj[b][a] = w
    return adj


def crow_flies(a, b) -> float:
    (x1, y1), (x2, y2) = POS[a], POS[b]
    return math.hypot(x2 - x1, y2 - y1)


def speed_limit() -> float:
    """The fewest minutes per map unit on any road: crow-flies distance times this never overestimates."""
    return min(w / crow_flies(a, b) for a, b, w in ROADS)


def a_star(adj: dict, start, goal, h) -> tuple[float, list | None, list]:
    """A* search (Figure 6.2): always expand the place with the smallest g + h.
    Returns (minutes, route, places expanded in order)."""
    g, parent = {start: 0}, {start: None}
    heap, done, expanded = [(h(start), start)], set(), []
    while heap:
        _, v = heapq.heappop(heap)
        if v in done:
            continue
        done.add(v)
        expanded.append(v)
        if v == goal:
            out = []
            while v is not None:
                out.append(v)
                v = parent[v]
            return g[goal], out[::-1], expanded
        for w, m in adj[v].items():
            if g[v] + m < g.get(w, float("inf")):
                g[w] = g[v] + m
                parent[w] = v
                heapq.heappush(heap, (g[w] + h(w), w))
    return float("inf"), None, expanded


def grid_graph(n: int, walls: set) -> dict:
    """An n x n grid of squares, one minute between open neighbours."""
    adj = {}
    for r in range(n):
        for c in range(n):
            if (r, c) in walls:
                continue
            adj[(r, c)] = {}
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (r + dr, c + dc)
                if 0 <= q[0] < n and 0 <= q[1] < n and q not in walls:
                    adj[(r, c)][q] = 1
    return adj


if __name__ == "__main__":
    adj, s = weighted_adjacency(), speed_limit()
    print(round(s, 3))
    print(a_star(adj, "Library", "Harbour", lambda v: 0))
    print(a_star(adj, "Library", "Harbour", lambda v: s * crow_flies(v, "Harbour")))
