"""Volume 8, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch02_examples import Graph, in_out_degrees


def find_judge(n: int, trust: list[tuple[int, int]]) -> int:
    """Exercise 1 (LeetCode 997): the town judge trusts nobody and is trusted by everyone else."""
    graph: Graph = {p: [] for p in range(1, n + 1)}
    for a, b in trust:
        graph[a].append(b)
    for p, (inn, out) in in_out_degrees(graph).items():
        if inn == n - 1 and out == 0:
            return p
    return -1


def max_edges(n: int, directed: bool) -> int:
    """Exercise 2: a complete graph has n(n-1)/2 undirected edges, or n(n-1) directed ones."""
    return n * (n - 1) if directed else n * (n - 1) // 2


def density(graph: Graph) -> float:
    """Exercise 3: edges present / edges possible (undirected)."""
    n = len(graph)
    edges = sum(len(v) for v in graph.values()) // 2
    return edges / max_edges(n, False) if n > 1 else 0.0


def sources_and_sinks(graph: Graph) -> tuple[list[Hashable], list[Hashable]]:
    """Exercise 4: directed vertices with no incoming edges (sources) and no outgoing edges (sinks)."""
    d = in_out_degrees(graph)
    return sorted(v for v in d if d[v][0] == 0), sorted(v for v in d if d[v][1] == 0)


if __name__ == "__main__":
    print(find_judge(3, [(1, 3), (2, 3)]), max_edges(5, False), max_edges(5, True))
    print(round(density({"a": ["b"], "b": ["a", "c"], "c": ["b"]}), 2), sources_and_sinks({"wake": ["dress"], "dress": ["school"], "school": []}))
