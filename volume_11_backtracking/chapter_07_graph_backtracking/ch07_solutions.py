"""Volume 11, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch07_examples import Graph


def all_hamiltonian_paths(graph: Graph, start: Hashable) -> list[list[Hashable]]:
    """Exercise 1: every path from start that visits each vertex once (not necessarily a cycle)."""
    out: list[list[Hashable]] = []
    path, on_path = [start], {start}

    def go() -> None:
        if len(path) == len(graph):
            out.append(list(path))
            return
        for w in graph[path[-1]]:
            if w not in on_path:
                path.append(w)
                on_path.add(w)
                go()
                path.pop()
                on_path.remove(w)

    go()
    return out


def is_proper_coloring(graph: Graph, color: dict) -> bool:
    """Exercise 2: every vertex coloured and no edge joins equal colours."""
    return set(color) == set(graph) and all(color[u] != color[v] for u in graph for v in graph[u])


def count_colorings(graph: Graph, m: int) -> int:
    """Exercise 3: how many proper colourings with m colours (the chromatic polynomial evaluated at m)."""
    order = list(graph)
    color: dict[Hashable, int] = {}

    def go(i: int) -> int:
        if i == len(order):
            return 1
        v = order[i]
        total = 0
        for c in range(m):
            if all(color.get(w) != c for w in graph[v]):
                color[v] = c
                total += go(i + 1)
                del color[v]
        return total

    return go(0)


if __name__ == "__main__":
    tri = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
    print(all_hamiltonian_paths(tri, "a"), count_colorings(tri, 3), is_proper_coloring(tri, {"a": 0, "b": 1, "c": 2}))
