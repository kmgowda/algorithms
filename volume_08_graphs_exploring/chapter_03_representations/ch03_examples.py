"""Volume 8, Chapter 3 - Representing Graphs: Adjacency Matrix vs. Adjacency List vs. Edge List.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import sys
from typing import Hashable


def edge_list_to_adjacency_list(n: int, edges: list[tuple[int, int]], directed: bool = False) -> list[list[int]]:
    """Vertices 0..n-1. Each vertex keeps a list of its neighbours: O(V + E) memory."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def edge_list_to_matrix(n: int, edges: list[tuple[int, int]], directed: bool = False) -> list[list[int]]:
    """An n x n grid of 0/1: matrix[u][v] = 1 if there's an edge. O(V^2) memory, O(1) edge checks."""
    m = [[0] * n for _ in range(n)]
    for u, v in edges:
        m[u][v] = 1
        if not directed:
            m[v][u] = 1
    return m


def matrix_to_edge_list(m: list[list[int]], directed: bool = False) -> list[tuple[int, int]]:
    n = len(m)
    return [(u, v) for u in range(n) for v in range(n) if m[u][v] and (directed or u < v)]


def has_edge_matrix(m: list[list[int]], u: int, v: int) -> bool:
    return bool(m[u][v])                                  # O(1)


def has_edge_list(adj: list[list[int]], u: int, v: int) -> bool:
    return v in adj[u]                                    # O(degree)


class LabeledGraph:
    """Real data has names, not numbers: map each label to an index once, then use fast integer lists."""

    def __init__(self) -> None:
        self.index: dict[Hashable, int] = {}
        self.labels: list[Hashable] = []
        self.adj: list[list[int]] = []

    def _id(self, label: Hashable) -> int:
        if label not in self.index:
            self.index[label] = len(self.labels)
            self.labels.append(label)
            self.adj.append([])
        return self.index[label]

    def add_edge(self, a: Hashable, b: Hashable, directed: bool = False) -> None:
        u, v = self._id(a), self._id(b)
        self.adj[u].append(v)
        if not directed:
            self.adj[v].append(u)

    def neighbours(self, label: Hashable) -> list[Hashable]:
        return [self.labels[v] for v in self.adj[self.index[label]]]


def memory_bytes(n: int, e: int) -> dict[str, int]:
    """Rough memory for the three representations on this Python (lists of ints)."""
    adj = edge_list_to_adjacency_list(n, [(i % n, (i * 7 + 1) % n) for i in range(e)])
    mat = [[0] * n for _ in range(n)]
    edges = [(i % n, (i * 7 + 1) % n) for i in range(e)]
    size = sys.getsizeof
    return {
        "edge list": size(edges) + sum(size(t) for t in edges),
        "adjacency list": size(adj) + sum(size(row) for row in adj),
        "adjacency matrix": size(mat) + sum(size(row) for row in mat),
    }


def flights_from(routes: list[tuple[str, str]], airport: str) -> list[str]:
    """Industry example: an airline's route table (an edge list) turned into a lookup by departure airport."""
    g = LabeledGraph()
    for a, b in routes:
        g.add_edge(a, b, directed=True)
    return sorted(g.neighbours(airport)) if airport in g.index else []


if __name__ == "__main__":
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    print("list:", edge_list_to_adjacency_list(4, edges))
    print("matrix:", edge_list_to_matrix(4, edges))
    print("back to edges:", matrix_to_edge_list(edge_list_to_matrix(4, edges)))
    print("memory for 10,000 vertices, 30,000 edges:", memory_bytes(10_000, 30_000))
    print("flights from BLR:", flights_from([("BLR", "DEL"), ("BLR", "BOM"), ("DEL", "BLR"), ("BOM", "GOI")], "BLR"))
