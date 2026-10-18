"""Volume 8, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations


def reverse_graph(adj: list[list[int]]) -> list[list[int]]:
    """Exercise 1: flip every directed edge (needed for Kosaraju's algorithm, Chapter 8)."""
    rev: list[list[int]] = [[] for _ in adj]
    for u, nbrs in enumerate(adj):
        for v in nbrs:
            rev[v].append(u)
    return rev


def matrix_to_list(m: list[list[int]]) -> list[list[int]]:
    """Exercise 2: matrix -> adjacency list in O(V^2)."""
    return [[v for v, bit in enumerate(row) if bit] for row in m]


def common_neighbours_matrix(m: list[list[int]], u: int, v: int) -> int:
    """Exercise 3: how many vertices are adjacent to both u and v - row AND row."""
    return sum(a & b for a, b in zip(m[u], m[v]))


def best_representation(vertices: int, edges: int, need_fast_edge_check: bool) -> str:
    """Exercise 4: a simple rule of thumb."""
    if need_fast_edge_check and vertices <= 5000:
        return "adjacency matrix"
    if edges < vertices * vertices // 8:
        return "adjacency list"
    return "adjacency matrix"


if __name__ == "__main__":
    print(reverse_graph([[1, 2], [2], []]), matrix_to_list([[0, 1], [1, 0]]),
          common_neighbours_matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0, 1), best_representation(10**6, 3 * 10**6, False))
