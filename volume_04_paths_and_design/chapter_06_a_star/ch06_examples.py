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


def a_star(adj: dict, start, goal, h, reopen: bool = False) -> tuple[float, list | None, list]:
    """A* search (Figure 6.2): always expand the place with the smallest g + h.
    reopen=False is the usual closed-set version, correct when h is consistent (Section 6.4);
    reopen=True lets an expanded place be expanded again if a cheaper route to it appears, which keeps
    any admissible guess correct. Returns (minutes, route, places expanded in order)."""
    g, parent = {start: 0}, {start: None}
    heap, done, expanded = [(h(start), start)], set(), []
    while heap:
        f, v = heapq.heappop(heap)
        if v in done or f > g[v] + h(v):
            continue                                  # an out-of-date heap entry
        done.add(v)
        expanded.append(v)
        if v == goal:
            out = []
            while v is not None:
                out.append(v)
                v = parent[v]
            return g[goal], out[::-1], expanded
        for w, m in adj[v].items():
            if w in done and not reopen:
                continue                              # closed for good
            if g[v] + m < g.get(w, float("inf")):
                g[w] = g[v] + m
                parent[w] = v
                done.discard(w)                       # reopened (only possible when reopen=True)
                heapq.heappush(heap, (g[w] + h(w), w))
    return float("inf"), None, expanded


def inconsistent_roads(adj: dict, h) -> list:
    """Roads v -> w that break consistency, h(v) <= m + h(w) (Section 6.4)."""
    return [(v, w) for v in adj for w, m in adj[v].items() if h(v) > m + h(w) + 1e-9]


def reduced_costs(adj: dict, h) -> dict:
    """The same map with each road v -> w costing m + h(w) - h(v): A* is Dijkstra on these costs."""
    return {v: {w: m + h(w) - h(v) for w, m in adj[v].items()} for v in adj}


# A small one-way map where an admissible guess that is not consistent fools the closed-set version (Figure 6.4).
TRAP = {"Start": {"A": 1, "C": 3}, "A": {"C": 1}, "C": {"Goal": 3}, "Goal": {}}
TRAP_H = {"Start": 0, "A": 4, "C": 0, "Goal": 0}


def true_remaining(adj: dict, goal) -> dict:
    """Exact minutes from every place to goal (Dijkstra on reversed roads): the perfect guess."""
    back = {v: {} for v in adj}
    for v in adj:
        for w, m in adj[v].items():
            back[w][v] = m
    dist, heap = {goal: 0}, [(0, goal)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue
        for w, m in back[v].items():
            if d + m < dist.get(w, float("inf")):
                dist[w] = d + m
                heapq.heappush(heap, (dist[w], w))
    return dist


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


# Figure 6.3: a wall with a gap at the top; Figure 6.5 (cases): a wall straight across the line of sight.
GAP_WALLS = {(r, 25) for r in range(8, 40)}
GAP_START, GAP_GOAL = (32, 5), (4, 36)
POCKET_WALLS = {(r, 20) for r in range(10, 31)}
POCKET_START, POCKET_GOAL = (20, 0), (20, 39)


def grid_distance(goal):
    return lambda v: abs(v[0] - goal[0]) + abs(v[1] - goal[1])


if __name__ == "__main__":
    adj, s = weighted_adjacency(), speed_limit()
    print(round(s, 3))
    print(a_star(adj, "Library", "Harbour", lambda v: 0))
    print(a_star(adj, "Library", "Harbour", lambda v: s * crow_flies(v, "Harbour")))
    print(a_star(TRAP, "Start", "Goal", TRAP_H.get)[:2], a_star(TRAP, "Start", "Goal", TRAP_H.get, reopen=True)[:2])
