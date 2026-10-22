"""Volume 5, Chapter 4 - Thinking Problems: counting the quickest walks (Thinking Problem 2) and the backward pass
run in the wrong order (Thinking Problem 3).

Run:  python3 ch04_solutions.py
"""

from __future__ import annotations

import ch04_examples as ex


def count_quickest_walks(vertices: list, edges: list, start) -> tuple[dict, dict]:
    """Quickest time from start to every vertex of a DAG and the number of different walks that achieve it.
    One pass in topological order: a strictly better offer resets the count, an equal offer adds to it."""
    order = ex.topological_order(vertices, edges)
    if order is None:
        raise ValueError("the graph has a cycle")
    out = {v: [] for v in vertices}
    for a, b, w in edges:
        out[a].append((b, w))
    dist, ways = {v: float("inf") for v in vertices}, {v: 0 for v in vertices}
    dist[start], ways[start] = 0, 1
    for v in order:
        if ways[v] == 0:
            continue                                  # not reachable
        for b, w in out[v]:
            if dist[v] + w < dist[b]:
                dist[b], ways[b] = dist[v] + w, ways[v]
            elif dist[v] + w == dist[b]:
                ways[b] += ways[v]
    return dist, ways


def latest_in_forward_order(hours: dict, before: list) -> dict:
    """The WRONG backward pass: latest starts computed in topological order instead of its reverse."""
    finish, earliest, _, _ = ex.critical_path(hours, before)
    order = ex.topological_order(list(hours), [(a, b, 0) for a, b in before])
    latest = {t: finish - hours[t] for t in hours}
    for t in order:
        for a, b in before:
            if a == t:
                latest[t] = min(latest[t], latest[b] - hours[t])
    return latest


if __name__ == "__main__":
    print(count_quickest_walks(ex.STOPS, ex.PATHS, "Gate"))
    print(latest_in_forward_order(ex.BUILD, ex.BEFORE))
