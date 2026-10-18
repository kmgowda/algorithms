"""Volume 8, Chapter 9 - Bipartite Graphs and Graph Coloring.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Hashable

Graph = dict[Hashable, list[Hashable]]


def two_color(graph: Graph) -> dict[Hashable, int] | None:
    """BFS colouring with 0/1: every neighbour must get the opposite colour.
    Returns the colouring, or None if some edge joins two same-coloured vertices (an odd cycle)."""
    color: dict[Hashable, int] = {}
    for start in graph:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for w in graph[v]:
                if w not in color:
                    color[w] = 1 - color[v]
                    queue.append(w)
                elif color[w] == color[v]:
                    return None
    return color


def is_bipartite(graph: Graph) -> bool:
    return two_color(graph) is not None


def odd_cycle(graph: Graph) -> list[Hashable] | None:
    """Proof of 'not bipartite': find an odd cycle using the BFS tree (parent pointers) of the clashing edge."""
    for start in graph:
        parent: dict[Hashable, Hashable | None] = {start: None}
        depth = {start: 0}
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for w in graph[v]:
                if w not in depth:
                    depth[w], parent[w] = depth[v] + 1, v
                    queue.append(w)
                elif depth[w] == depth[v]:                     # same level -> odd cycle through their common ancestor
                    a, b, left, right = v, w, [v], [w]
                    while a != b:
                        a, b = parent[a], parent[b]           # type: ignore[assignment]
                        left.append(a)
                        right.append(b)
                    return left + right[-2::-1]
    return None


def greedy_coloring(graph: Graph, order: list[Hashable] | None = None) -> dict[Hashable, int]:
    """Give each vertex the smallest colour not used by an already-coloured neighbour.
    Uses at most (max degree + 1) colours - not always the minimum (finding the minimum is NP-hard)."""
    color: dict[Hashable, int] = {}
    for v in order or list(graph):
        taken = {color[w] for w in graph[v] if w in color}
        c = 0
        while c in taken:
            c += 1
        color[v] = c
    return color


def welsh_powell(graph: Graph) -> dict[Hashable, int]:
    """Greedy colouring, busiest vertices first - often fewer colours in practice."""
    return greedy_coloring(graph, sorted(graph, key=lambda v: (-len(graph[v]), str(v))))


def exam_timetable(clashes: list[tuple[str, str]]) -> dict[str, int]:
    """Industry example: exams sharing a student can't be in the same slot. Colours = time slots."""
    graph: Graph = {}
    for a, b in clashes:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)
    return welsh_powell(graph)                                # type: ignore[return-value]


if __name__ == "__main__":
    teams = {"Ana": ["Ben", "Dev"], "Ben": ["Ana", "Cy"], "Cy": ["Ben", "Dev"], "Dev": ["Cy", "Ana"]}
    print("4-cycle bipartite:", two_color(teams))
    triangle = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
    print("triangle bipartite:", is_bipartite(triangle), "| odd cycle:", odd_cycle(triangle))
    print("exam slots:", exam_timetable([("Maths", "Physics"), ("Maths", "Chemistry"), ("Physics", "Biology"),
                                         ("Chemistry", "Biology"), ("Maths", "Biology")]))
