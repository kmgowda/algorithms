"""Volume 5, Chapter 1 - The Shortest-Path Problem: roads with lengths, and why counting roads is not enough.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from collections import deque

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]


def weighted_adjacency(places=PLACES, roads=ROADS) -> dict:
    """Each place maps to {neighbour: minutes}; roads go both ways (Figure 1.1)."""
    adj = {p: {} for p in places}
    for a, b, w in roads:
        adj[a][b] = w
        adj[b][a] = w
    return adj


def route_length(adj: dict, route: list) -> float:
    """Total minutes along a route; infinity if two consecutive places are not joined by a road."""
    total = 0
    for a, b in zip(route, route[1:]):
        if b not in adj[a]:
            return float("inf")
        total += adj[a][b]
    return total


def all_routes(adj: dict, start, goal, path=None):
    """Every route from start to goal that never repeats a place (the table of Section 1.5)."""
    path = path or [start]
    if path[-1] == goal:
        yield list(path)
        return
    for w in adj[path[-1]]:
        if w not in path:
            yield from all_routes(adj, start, goal, path + [w])


def shortest_by_brute_force(adj: dict, start, goal) -> tuple[float, list | None, int]:
    """Try every route and keep the quickest. Returns (minutes, route, routes tried)."""
    best, best_route, tried = float("inf"), None, 0
    for r in all_routes(adj, start, goal):
        tried += 1
        length = route_length(adj, r)
        if length < best:
            best, best_route = length, r
    return best, best_route, tried


def fewest_roads_route(adj: dict, start, goal) -> list | None:
    """Volume 4's breadth-first search: the route with the fewest roads, ignoring their lengths."""
    parent, queue = {start: None}, deque([start])
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w not in parent:
                parent[w] = v
                queue.append(w)
    if goal not in parent:
        return None
    out = []
    while goal is not None:
        out.append(goal)
        goal = parent[goal]
    return out[::-1]


def prefix_lengths(adj: dict, route: list) -> list:
    """Section 1.5: (place, minutes along the route so far, quickest possible minutes) for every stop on a route.
    On a shortest route the two numbers always agree: every first part of a shortest route is itself shortest."""
    out = []
    for i in range(len(route)):
        so_far = route_length(adj, route[:i + 1])
        out.append((route[i], so_far, shortest_by_brute_force(adj, route[0], route[i])[0]))
    return out


def state_graph(adj: dict, via) -> dict:
    """Section 1.5: an implicit graph whose vertices are states (place, collected?). A van must pick up a parcel at
    `via` before the end; arriving at `via` switches the state from False to True. Same minutes as the town."""
    states = {}
    for p in adj:
        for got in (False, True):
            states[(p, got)] = {}
    for p in adj:
        for q, w in adj[p].items():
            for got in (False, True):
                states[(p, got)][(q, got or q == via)] = w
    return states


def quickest_via(adj: dict, start, via, goal) -> tuple[float, list | None, int]:
    """The quickest route from start to goal that passes through via, found by brute force on the state graph.
    Returns (minutes, list of places, number of states)."""
    g = state_graph(adj, via)
    minutes, r, _ = shortest_by_brute_force(g, (start, start == via), (goal, True))
    return minutes, (None if r is None else [p for p, _ in r]), len(g)


if __name__ == "__main__":
    adj = weighted_adjacency()
    bfs = fewest_roads_route(adj, "Library", "Harbour")
    print(bfs, route_length(adj, bfs))
    print(shortest_by_brute_force(adj, "Library", "Harbour"))
    for r in sorted(all_routes(adj, "Library", "Harbour"), key=lambda r: route_length(adj, r))[:6]:
        print(route_length(adj, r), r)
