"""Volume 4, Chapter 20 - Breadth-First Search: explore in layers, find routes with the fewest roads.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

from collections import deque

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]


def adjacency(places=PLACES, roads=ROADS) -> dict:
    adj = {p: [] for p in places}
    for a, b in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def bfs(adj: dict, start, log: list | None = None) -> tuple[dict, dict]:
    """Distances in roads and the parent of each place (Figure 20.2): the frontier is a queue."""
    dist, parent = {start: 0}, {start: None}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                parent[w] = v
                queue.append(w)
        if log is not None:
            log.append((v, list(queue)))
    return dist, parent


def route(parent: dict, goal) -> list | None:
    """Walk the parent links back from the goal and reverse (Section 20.5); None if the goal was never reached."""
    if goal not in parent:
        return None
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]


def layers(dist: dict) -> list[list]:
    out = []
    for v, d in dist.items():
        while len(out) <= d:
            out.append([])
        out[d].append(v)
    return out


def count_shortest_routes(adj: dict, start) -> dict:
    """Section 20.6: number of fewest-roads routes to each place = sum over neighbours one layer nearer."""
    dist, _ = bfs(adj, start)
    count = {start: 1}
    for v in sorted(dist, key=dist.get):
        for w in adj[v]:
            if dist.get(w) == dist[v] + 1:
                count[w] = count.get(w, 0) + count[v]
    return count


if __name__ == "__main__":
    adj = adjacency()
    log = []
    dist, parent = bfs(adj, "Library", log)
    print(dist)
    print(layers(dist))
    for row in log:
        print(row)
    print(route(parent, "Harbour"), route(parent, "Museum"))
