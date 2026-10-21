"""Volume 3, Chapter 22 - Walking a Graph: the town map, adjacency lists, and the generic explore loop.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]


def adjacency(places=PLACES, roads=ROADS) -> dict[str, list[str]]:
    """Neighbour lists, in the order the roads are listed (Figure 22.2)."""
    adj = {p: [] for p in places}
    for a, b, _ in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def explore(adj: dict, start, log: list | None = None) -> list:
    """The generic walk (Figure 22.3): keep a frontier of places seen but not yet visited, and a visited set.
    Taking from the end of the frontier makes it a stack; Chapter 23 takes from the front instead."""
    visited, frontier, order = {start}, [start], []
    while frontier:
        v = frontier.pop()
        order.append(v)
        for w in adj[v]:
            if w not in visited:
                visited.add(w)
                frontier.append(w)
        if log is not None:
            log.append((v, list(frontier)))
    return order


def reachable(adj: dict, start) -> set:
    return set(explore(adj, start))


def degree_table(adj: dict) -> dict:
    return {v: len(ws) for v, ws in adj.items()}


if __name__ == "__main__":
    adj = adjacency()
    for v in PLACES:
        print(v, adj[v])
    log = []
    print(explore(adj, "Library", log))
    for row in log:
        print(row)
    print(degree_table(adj), sum(degree_table(adj).values()), len(ROADS))
