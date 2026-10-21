"""Volume 4, Chapter 4 - Shortest Paths in a DAG: relax roads in topological order, one pass.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

# The book-festival trail: one-way paths downhill from the Gate; minutes for each path (some are shortcuts on bikes).
STOPS = ["Gate", "Poetry", "Maps", "Science", "Stories", "Cafe", "Stage"]
PATHS = [("Gate", "Poetry", 5), ("Gate", "Maps", 3), ("Maps", "Poetry", 1), ("Poetry", "Science", 6),
         ("Maps", "Science", 7), ("Maps", "Stories", 4), ("Poetry", "Stories", 2), ("Science", "Cafe", 1),
         ("Stories", "Cafe", 6), ("Stories", "Science", -2), ("Science", "Stage", 5), ("Cafe", "Stage", 2)]


def topological_order(vertices: list, edges: list) -> list | None:
    """Kahn's method (Volume 3, Chapter 27); None if the graph has a cycle."""
    indeg = {v: 0 for v in vertices}
    for _, b, _ in edges:
        indeg[b] += 1
    ready = [v for v in vertices if indeg[v] == 0]
    order = []
    while ready:
        v = ready.pop(0)
        order.append(v)
        for a, b, _ in edges:
            if a == v:
                indeg[b] -= 1
                if indeg[b] == 0:
                    ready.append(b)
    return order if len(order) == len(vertices) else None


def dag_shortest(vertices: list, edges: list, start, longest: bool = False) -> tuple[dict, dict, list]:
    """Relax each vertex's edges once, in topological order (Figure 4.2). longest=True finds longest paths instead.
    Returns (dist, parent, order)."""
    order = topological_order(vertices, edges)
    if order is None:
        raise ValueError("the graph has a cycle")
    inf = float("inf")
    worse = -inf if longest else inf
    dist = {v: worse for v in vertices}
    parent = {v: None for v in vertices}
    dist[start] = 0
    better = (lambda x, y: x > y) if longest else (lambda x, y: x < y)
    for v in order:
        if dist[v] == worse:
            continue                                  # not reachable from the start (yet, or ever)
        for a, b, w in edges:
            if a == v and better(dist[v] + w, dist[b]):
                dist[b] = dist[v] + w
                parent[b] = v
    return dist, parent, order


def route(parent: dict, goal) -> list:
    out = []
    while goal is not None:
        out.append(goal)
        goal = parent[goal]
    return out[::-1]


if __name__ == "__main__":
    dist, parent, order = dag_shortest(STOPS, PATHS, "Gate")
    print(order)
    print(dist, route(parent, "Stage"))
    ld, lp, _ = dag_shortest(STOPS, PATHS, "Gate", longest=True)
    print(ld, route(lp, "Stage"))
