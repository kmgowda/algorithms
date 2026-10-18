"""Volume 8, Chapter 4 - Depth-First Search: Exploring a Maze.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

from typing import Hashable

Graph = dict[Hashable, list[Hashable]]


def dfs_recursive(graph: Graph, start: Hashable) -> list[Hashable]:
    """Go as deep as possible along one corridor; back up only at dead ends. Returns the visiting order."""
    order: list[Hashable] = []
    visited: set[Hashable] = set()

    def visit(v: Hashable) -> None:
        visited.add(v)
        order.append(v)
        for w in graph.get(v, []):
            if w not in visited:
                visit(w)

    visit(start)
    return order


def dfs_iterative(graph: Graph, start: Hashable) -> list[Hashable]:
    """The same order with an explicit stack (V2-C8) - no recursion limit.
    Neighbours are pushed in reverse so the first neighbour is explored first, matching the recursive version."""
    order, visited, stack = [], set(), [start]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        order.append(v)
        for w in reversed(graph.get(v, [])):
            if w not in visited:
                stack.append(w)
    return order


def find_path(graph: Graph, start: Hashable, goal: Hashable) -> list[Hashable] | None:
    """A path (not necessarily shortest) from start to goal: remember each vertex's 'parent', then walk back."""
    parent: dict[Hashable, Hashable | None] = {start: None}
    stack = [start]
    while stack:
        v = stack.pop()
        if v == goal:
            path = []
            while v is not None:
                path.append(v)
                v = parent[v]
            return path[::-1]
        for w in graph.get(v, []):
            if w not in parent:
                parent[w] = v
                stack.append(w)
    return None


def discovery_finish_times(graph: Graph) -> tuple[dict[Hashable, int], dict[Hashable, int]]:
    """Time stamps when DFS first reaches a vertex and when it finishes it (used in Chapters 7, 8, 10)."""
    disc: dict[Hashable, int] = {}
    fin: dict[Hashable, int] = {}
    clock = 0

    def visit(v: Hashable) -> None:
        nonlocal clock
        disc[v] = clock
        clock += 1
        for w in graph.get(v, []):
            if w not in disc:
                visit(w)
        fin[v] = clock
        clock += 1

    for v in graph:
        if v not in disc:
            visit(v)
    return disc, fin


def maze_rooms(maze: Graph, entrance: str, treasure: str) -> list[str] | None:
    """Beginner example: rooms connected by doors; find a way from the entrance to the treasure."""
    return find_path(maze, entrance, treasure)


def can_unlock_all(rooms: list[list[int]]) -> bool:
    """Industry example (LeetCode 841): room i holds keys to other rooms; starting in room 0, can we open all?
    Same as: does DFS from 0 reach every vertex? (Think: services that grant access to other services.)"""
    graph = {i: keys for i, keys in enumerate(rooms)}
    return len(dfs_iterative(graph, 0)) == len(rooms)


if __name__ == "__main__":
    g = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["F"], "F": []}
    print("recursive:", dfs_recursive(g, "A"), "| iterative:", dfs_iterative(g, "A"))
    print("path A->F:", find_path(g, "A", "F"))
    disc, fin = discovery_finish_times(g)
    print("discover/finish:", {v: (disc[v], fin[v]) for v in g})
    maze = {"entrance": ["hall"], "hall": ["entrance", "library", "kitchen"], "library": ["hall", "secret room"],
            "kitchen": ["hall"], "secret room": ["library", "treasure"], "treasure": ["secret room"]}
    print(maze_rooms(maze, "entrance", "treasure"))
    print(can_unlock_all([[1], [2], [3], []]), can_unlock_all([[1, 3], [3, 0, 1], [2], [0]]))
