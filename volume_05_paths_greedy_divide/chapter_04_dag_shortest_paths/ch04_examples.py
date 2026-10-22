"""Volume 5, Chapter 4 - Shortest Paths in a DAG: relax roads in topological order, one pass.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

from collections import deque

# The book-festival trail: one-way paths downhill from the Gate; minutes for each path (some are shortcuts on bikes).
STOPS = ["Gate", "Poetry", "Maps", "Science", "Stories", "Cafe", "Stage"]
PATHS = [("Gate", "Poetry", 5), ("Gate", "Maps", 3), ("Maps", "Poetry", 1), ("Poetry", "Science", 6),
         ("Maps", "Science", 7), ("Maps", "Stories", 4), ("Poetry", "Stories", 2), ("Science", "Cafe", 1),
         ("Stories", "Cafe", 6), ("Stories", "Science", -2), ("Science", "Stage", 5), ("Cafe", "Stage", 2)]


def topological_order(vertices: list, edges: list) -> list | None:
    """Kahn's method (Volume 4, Chapter 24); None if the graph has a cycle. O(V + E) with out-lists."""
    indeg, out = {v: 0 for v in vertices}, {v: [] for v in vertices}
    for a, b, _ in edges:
        indeg[b] += 1
        out[a].append(b)
    ready = deque(v for v in vertices if indeg[v] == 0)
    order = []
    while ready:
        v = ready.popleft()
        order.append(v)
        for b in out[v]:
            indeg[b] -= 1
            if indeg[b] == 0:
                ready.append(b)
    return order if len(order) == len(vertices) else None


def dag_shortest(vertices: list, edges: list, start, longest: bool = False) -> tuple[dict, dict, list]:
    """Relax each vertex's edges once, in topological order (Section 4.4). longest=True finds longest paths.
    Returns (dist, parent, order)."""
    order = topological_order(vertices, edges)
    if order is None:
        raise ValueError("the graph has a cycle")
    worse = float("-inf") if longest else float("inf")
    better = (lambda x, y: x > y) if longest else (lambda x, y: x < y)
    dist, parent = {v: worse for v in vertices}, {v: None for v in vertices}
    dist[start] = 0
    out = {v: [] for v in vertices}
    for a, b, w in edges:
        out[a].append((b, w))
    for v in order:
        if dist[v] == worse:
            continue                                  # not reachable from the start
        for b, w in out[v]:
            if better(dist[v] + w, dist[b]):
                dist[b] = dist[v] + w
                parent[b] = v
    return dist, parent, order


def route(parent: dict, goal) -> list:
    out = []
    while goal is not None:
        out.append(goal)
        goal = parent[goal]
    return out[::-1]


# The festival build (Section 4.5, Figure 4.3): hours for each task, and which tasks must finish before it starts.
BUILD = {"frame": 3, "tents": 5, "lights": 2, "sound": 4, "signs": 1, "rehearsal": 2}
BEFORE = [("frame", "lights"), ("frame", "sound"), ("tents", "signs"), ("lights", "rehearsal"),
          ("sound", "rehearsal"), ("signs", "rehearsal")]


def critical_path(hours: dict, before: list) -> tuple[int, dict, dict, list]:
    """Earliest and latest start of every task, by one forward and one backward pass in topological order.
    Returns (finish time, earliest, latest, critical tasks with zero slack, in order)."""
    tasks = list(hours)
    order = topological_order(tasks, [(a, b, 0) for a, b in before])
    if order is None:
        raise ValueError("the plan has a cycle")
    earliest = {t: 0 for t in tasks}
    for t in order:                                   # forward: a task starts when its last prerequisite ends
        for a, b in before:
            if a == t:
                earliest[b] = max(earliest[b], earliest[t] + hours[t])
    finish = max((earliest[t] + hours[t] for t in tasks), default=0)
    latest = {t: finish - hours[t] for t in tasks}
    for t in reversed(order):                         # backward: a task must end before its first follower starts
        for a, b in before:
            if a == t:
                latest[t] = min(latest[t], latest[b] - hours[t])
    critical = [t for t in order if latest[t] == earliest[t]]
    return finish, earliest, latest, critical


if __name__ == "__main__":
    dist, parent, order = dag_shortest(STOPS, PATHS, "Gate")
    print(order)
    print(dist, route(parent, "Stage"))
    ld, lp, _ = dag_shortest(STOPS, PATHS, "Gate", longest=True)
    print(ld, route(lp, "Stage"))
