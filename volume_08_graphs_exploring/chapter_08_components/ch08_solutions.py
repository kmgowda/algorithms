"""Volume 8, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch08_examples import Graph, condensation, connected_components, kosaraju_scc


def is_strongly_connected(graph: Graph) -> bool:
    """Exercise 1: one SCC containing everything."""
    return len(kosaraju_scc(graph)) == 1


def min_roads_to_connect(n: int, roads: list[tuple[int, int]]) -> int:
    """Exercise 2 (LeetCode 1319 idea): with k separate components, k - 1 new roads join them all."""
    graph: Graph = {v: [] for v in range(n)}
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    return len(connected_components(graph)) - 1


def min_new_one_way_links(graph: Graph) -> int:
    """Exercise 3: fewest one-way edges to make a directed graph strongly connected
    = max(#source SCCs, #sink SCCs) in the condensation (0 if already one SCC)."""
    _, dag = condensation(graph)
    if len(dag) == 1:
        return 0
    has_in = {v for targets in dag.values() for v in targets}
    sources = sum(1 for c in dag if c not in has_in)
    sinks = sum(1 for c in dag if not dag[c])
    return max(sources, sinks)


def largest_group(graph: Graph) -> list[Hashable]:
    """Exercise 4: the biggest connected component (e.g. the largest friend circle)."""
    return max(connected_components(graph), key=len)


if __name__ == "__main__":
    print(is_strongly_connected({1: [2], 2: [3], 3: [1]}), min_roads_to_connect(6, [(0, 1), (2, 3)]),
          min_new_one_way_links({1: [2], 2: [3], 3: []}), largest_group({1: [2], 2: [1, 3], 3: [2], 4: []}))
