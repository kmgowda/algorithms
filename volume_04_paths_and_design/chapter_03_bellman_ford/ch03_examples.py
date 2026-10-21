"""Volume 4, Chapter 3 - Negative Roads: Bellman-Ford relaxes every road, round after round.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

# The courier's one-way legs between depots: a negative weight is a bonus paid for carrying a parcel.
DEPOTS = ["A", "B", "C", "D", "E"]
LEGS = [("A", "B", 6), ("A", "C", 7), ("B", "C", 8), ("B", "D", 5), ("B", "E", -4), ("C", "D", -3), ("C", "E", 9),
        ("D", "B", -2), ("E", "D", 7), ("E", "A", 2)]


def bellman_ford(vertices: list, edges: list, start, log: list | None = None) -> tuple[dict, dict, bool]:
    """Shortest distances with negative weights allowed (Figure 3.2).
    Returns (dist, parent, has_negative_cycle). Up to V - 1 rounds, then one extra round to detect a cycle."""
    inf = float("inf")
    dist = {v: inf for v in vertices}
    parent = {v: None for v in vertices}
    dist[start] = 0
    for rnd in range(1, len(vertices)):
        changed = False
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                parent[b] = a
                changed = True
        if log is not None:
            log.append((rnd, dict(dist)))
        if not changed:
            break                                     # nothing improved: every distance is final
    cycle = any(dist[a] + w < dist[b] for a, b, w in edges)
    return dist, parent, cycle


def route(parent: dict, goal) -> list:
    out = []
    while goal is not None:
        out.append(goal)
        goal = parent[goal]
    return out[::-1]


if __name__ == "__main__":
    log = []
    dist, parent, cycle = bellman_ford(DEPOTS, LEGS, "A", log)
    for rnd, d in log:
        print(rnd, d)
    print(dist, cycle, route(parent, "D"), route(parent, "E"))
