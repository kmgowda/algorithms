"""Volume 8, Chapter 7 - Cycle Detection and Topological Sort: Course Schedules and Build Systems.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Hashable

Graph = dict[Hashable, list[Hashable]]

WHITE, GRAY, BLACK = 0, 1, 2


def has_cycle_directed(graph: Graph) -> bool:
    """DFS colours: WHITE unseen, GRAY on the current path, BLACK finished.
    Reaching a GRAY vertex again means we've come back around a loop. Iterative, so long chains are fine."""
    color = {v: WHITE for v in graph}
    for root in graph:
        if color[root] != WHITE:
            continue
        color[root] = GRAY
        stack = [(root, iter(graph[root]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                color[v] = BLACK
                stack.pop()
            elif color.get(w, WHITE) == GRAY:
                return True
            elif color.get(w, WHITE) == WHITE:
                color[w] = GRAY
                stack.append((w, iter(graph.get(w, []))))
    return False


def has_cycle_undirected(graph: Graph) -> bool:
    """Undirected: a cycle exists if DFS meets a visited vertex that isn't the one it just came from."""
    seen: set[Hashable] = set()
    for root in graph:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, None)]
        while stack:
            v, parent = stack.pop()
            for w in graph[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append((w, v))
                elif w != parent:
                    return True
    return False


def topological_sort_kahn(graph: Graph) -> list[Hashable] | None:
    """Kahn's algorithm: repeatedly take a task with no remaining prerequisites.
    Edge u -> v means 'u must come before v'. Returns None if a cycle makes ordering impossible."""
    indegree = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] = indegree.get(v, 0) + 1
    ready = deque(v for v in indegree if indegree[v] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in graph.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    return order if len(order) == len(indegree) else None


def topological_sort_dfs(graph: Graph) -> list[Hashable] | None:
    """DFS version: a vertex is finished only after everything it points to; reversed finish order is a valid order."""
    color = {v: WHITE for v in graph}
    finished: list[Hashable] = []
    for root in graph:
        if color[root] != WHITE:
            continue
        color[root] = GRAY
        stack = [(root, iter(graph[root]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                color[v] = BLACK
                finished.append(v)
                stack.pop()
            elif color.get(w, WHITE) == GRAY:
                return None
            elif color.get(w, WHITE) == WHITE:
                color[w] = GRAY
                stack.append((w, iter(graph.get(w, []))))
    return finished[::-1]


def course_order(n: int, prerequisites: list[tuple[int, int]]) -> list[int]:
    """Beginner example (LeetCode 210): (course, prereq) pairs. An order to take all courses, or [] if impossible."""
    graph: Graph = {c: [] for c in range(n)}
    for course, pre in prerequisites:
        graph[pre].append(course)
    order = topological_sort_kahn(graph)
    return [] if order is None else list(order)        # type: ignore[arg-type]


def build_order(deps: dict[str, list[str]]) -> list[str] | None:
    """Industry example: a build tool. deps[target] = what it needs. Build needs before the targets that use them."""
    graph: Graph = {t: [] for t in deps}
    for target, needs in deps.items():
        for need in needs:
            graph.setdefault(need, []).append(target)
    order = topological_sort_kahn(graph)
    return order                                        # type: ignore[return-value]


if __name__ == "__main__":
    print(course_order(4, [(1, 0), (2, 0), (3, 1), (3, 2)]), course_order(2, [(0, 1), (1, 0)]))
    deps = {"app": ["ui", "db"], "ui": ["widgets"], "db": ["driver"], "widgets": [], "driver": []}
    print("build:", build_order(deps))
    print("directed cycle?", has_cycle_directed({"a": ["b"], "b": ["c"], "c": ["a"]}),
          "| undirected cycle?", has_cycle_undirected({"a": ["b"], "b": ["a", "c"], "c": ["b"]}))
    print("DFS order:", topological_sort_dfs({"wake": ["dress"], "dress": ["shoes", "breakfast"], "breakfast": ["school"],
                                              "shoes": ["school"], "school": []}))
