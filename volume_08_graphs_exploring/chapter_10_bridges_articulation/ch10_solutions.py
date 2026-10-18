"""Volume 8, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch10_examples import Graph, bridges


def count_components(graph: Graph, removed_vertex: Hashable | None = None,
                     removed_edge: tuple[Hashable, Hashable] | None = None) -> int:
    """Exercise 1: the brute-force check - delete something and count pieces with DFS."""
    seen: set[Hashable] = set()
    count = 0
    for s in graph:
        if s == removed_vertex or s in seen:
            continue
        count += 1
        seen.add(s)
        stack = [s]
        while stack:
            v = stack.pop()
            for w in graph[v]:
                if w == removed_vertex or w in seen:
                    continue
                if removed_edge and {v, w} == set(removed_edge):
                    continue
                seen.add(w)
                stack.append(w)
    return count


def two_edge_connected_groups(graph: Graph) -> list[list[Hashable]]:
    """Exercise 2: remove every bridge; what's left are the groups that survive any single cable cut."""
    cut = {frozenset(e) for e in bridges(graph)}
    seen: set[Hashable] = set()
    groups = []
    for s in graph:
        if s in seen:
            continue
        seen.add(s)
        stack, comp = [s], []
        while stack:
            v = stack.pop()
            comp.append(v)
            for w in graph[v]:
                if w not in seen and frozenset((v, w)) not in cut:
                    seen.add(w)
                    stack.append(w)
        groups.append(sorted(comp, key=str))
    return sorted(groups, key=lambda g: str(g[0]))


def cables_to_add_for_redundancy(graph: Graph) -> int:
    """Exercise 3: a connected network becomes bridge-free by adding ceil(leaves / 2) cables,
    where leaves are bridge-tree groups touched by exactly one bridge."""
    groups = two_edge_connected_groups(graph)
    if len(groups) == 1:
        return 0
    group_of = {v: i for i, g in enumerate(groups) for v in g}
    degree = [0] * len(groups)
    for a, b in bridges(graph):
        degree[group_of[a]] += 1
        degree[group_of[b]] += 1
    leaves = sum(1 for d in degree if d == 1)
    return (leaves + 1) // 2


if __name__ == "__main__":
    g = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    print(count_components(g, removed_vertex=1), two_edge_connected_groups(g), cables_to_add_for_redundancy(g))
