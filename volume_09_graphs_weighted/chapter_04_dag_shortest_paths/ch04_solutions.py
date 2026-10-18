"""Volume 9, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch04_examples import WGraph, topological_order


def count_paths(graph: WGraph, source: Hashable, target: Hashable) -> int:
    """Exercise 1: number of different routes in a DAG - add counts in topological order."""
    ways = {v: 0 for v in topological_order(graph)}
    ways[source] = 1
    for u in topological_order(graph):
        for v in graph.get(u, {}):
            ways[v] += ways[u]
    return ways[target]


def slack(tasks: dict[str, tuple[float, list[str]]]) -> dict[str, float]:
    """Exercise 2: how long each task can be delayed without delaying the project (critical tasks have 0)."""
    graph: WGraph = {t: {} for t in tasks}
    for t, (_, pre) in tasks.items():
        for p in pre:
            graph[p][t] = 1
    order = topological_order(graph)
    earliest: dict[str, float] = {}
    for t in order:
        earliest[t] = max((earliest[p] + tasks[p][0] for p in tasks[t][1]), default=0.0)
    project = max(earliest[t] + tasks[t][0] for t in tasks)
    latest: dict[str, float] = {}
    for t in reversed(order):
        latest_finish = min((latest[s] for s in graph[t]), default=project)
        latest[t] = latest_finish - tasks[t][0]
    return {t: latest[t] - earliest[t] for t in tasks}


def max_points_route(rows: list[list[int]]) -> int:
    """Exercise 3: a triangle of fruit trees - walk down to an adjacent tree each row, collecting the most fruit.
    The triangle is a DAG; longest path = most fruit."""
    best = rows[-1][:]
    for r in range(len(rows) - 2, -1, -1):
        best = [rows[r][i] + max(best[i], best[i + 1]) for i in range(len(rows[r]))]
    return best[0]


if __name__ == "__main__":
    print(count_paths({"a": {"b": 1, "c": 1}, "b": {"d": 1}, "c": {"d": 1}, "d": {}}, "a", "d"))
    house = {"foundation": (5, []), "walls": (7, ["foundation"]), "plumbing": (3, ["foundation"]),
             "roof": (4, ["walls"]), "electrics": (2, ["walls", "plumbing"]), "paint": (3, ["roof", "electrics"])}
    print(slack(house), max_points_route([[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]))
