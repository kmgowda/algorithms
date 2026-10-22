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
    """Quickest minutes to every reachable place and each place's parent (Figure 2.4). Weights must be >= 0."""
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


def offer_counts(adj: dict, start) -> tuple[int, int]:
    """Split the successful relaxations into first offers (a place gets its first time) and improvements
    (a place already offered gets a quicker time). The town: 7 first offers and 3 improvements."""
    dist, heap, settled, first, better = {start: 0}, [(0, start)], set(), 0, 0
    while heap:
        d, v = heapq.heappop(heap)
        if v in settled:
            continue
        settled.add(v)
        for w, minutes in adj[v].items():
            if d + minutes < dist.get(w, float("inf")):
                if w in dist:
                    better += 1
                else:
                    first += 1
                dist[w] = d + minutes
                heapq.heappush(heap, (dist[w], w))
    return first, better


def snapshots(adj: dict, start) -> list:
    """After each settle: (place settled, set of settled places, copy of the tentative times) (Figure 2.2)."""
    dist, heap, settled, out = {start: 0}, [(0, start)], set(), []
    while heap:
        d, v = heapq.heappop(heap)
        if v in settled:
            continue
        settled.add(v)
        for w, minutes in adj[v].items():
            if d + minutes < dist.get(w, float("inf")):
                dist[w] = d + minutes
                heapq.heappush(heap, (dist[w], w))
        out.append((v, set(settled), dict(dist)))
    return out


def dijkstra_array(adj: dict, start) -> tuple[dict, int]:
    """Dijkstra without a heap: scan every unsettled place for the smallest time (Section 2.5).
    Returns (dist, places looked at while scanning); the scans cost O(V^2) in all."""
    inf = float("inf")
    dist = {v: inf for v in adj}
    dist[start] = 0
    unsettled, looked = set(adj), 0
    while unsettled:
        looked += len(unsettled)
        v = min(unsettled, key=lambda u: dist[u])
        if dist[v] == inf:
            break                                     # the rest cannot be reached
        unsettled.remove(v)
        for w, minutes in adj[v].items():
            if dist[v] + minutes < dist[w]:
                dist[w] = dist[v] + minutes
    return {v: d for v, d in dist.items() if d < inf}, looked


if __name__ == "__main__":
    adj = weighted_adjacency()
    log = []
    dist, parent = dijkstra(adj, "Library", log)
    print(log)
    print(dist)
    print(route(parent, "Harbour"), route(parent, "Station"))
    print(dijkstra_counting(adj, "Library"))
