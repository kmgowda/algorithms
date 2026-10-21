"""Volume 4, Chapter 2 - Dijkstra's Algorithm: settle the nearest unsettled place, again and again.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import heapq

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]


def weighted_adjacency(places=PLACES, roads=ROADS) -> dict:
    adj = {p: {} for p in places}
    for a, b, w in roads:
        adj[a][b] = w
        adj[b][a] = w
    return adj


def dijkstra(adj: dict, start, log: list | None = None) -> tuple[dict, dict]:
    """Quickest minutes to every reachable place and each place's parent (Figure 2.3). Weights must be >= 0."""
    dist, parent = {start: 0}, {start: None}
    heap, settled = [(0, start)], set()
    while heap:
        d, v = heapq.heappop(heap)
        if v in settled:
            continue                                  # an out-of-date entry: v was settled more cheaply
        settled.add(v)
        if log is not None:
            log.append((v, d))
        for w, minutes in adj[v].items():
            if d + minutes < dist.get(w, float("inf")):
                dist[w] = d + minutes                 # relax: a quicker way to w, through v
                parent[w] = v
                heapq.heappush(heap, (dist[w], w))
    return dist, parent


def route(parent: dict, goal) -> list | None:
    if goal not in parent:
        return None
    out = []
    while goal is not None:
        out.append(goal)
        goal = parent[goal]
    return out[::-1]


def dijkstra_counting(adj: dict, start) -> tuple[dict, int, int]:
    """Dijkstra again, counting heap pushes and relaxations that improved a distance."""
    dist, heap, settled, pushes, improved = {start: 0}, [(0, start)], set(), 1, 0
    while heap:
        d, v = heapq.heappop(heap)
        if v in settled:
            continue
        settled.add(v)
        for w, minutes in adj[v].items():
            if d + minutes < dist.get(w, float("inf")):
                dist[w] = d + minutes
                improved += 1
                heapq.heappush(heap, (dist[w], w))
                pushes += 1
    return dist, pushes, improved


if __name__ == "__main__":
    adj = weighted_adjacency()
    log = []
    dist, parent = dijkstra(adj, "Library", log)
    print(log)
    print(dist)
    print(route(parent, "Harbour"), route(parent, "Station"))
    print(dijkstra_counting(adj, "Library"))
