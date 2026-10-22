"""Volume 4, Chapter 1 - Representing Graphs: companion code for the Thinking Problems (Section 1.17).

Run:  python3 ch01_solutions.py
"""

from __future__ import annotations


def compressed_from_edges(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    """Thinking Problem 2: the compressed form of a directed graph on vertices 0..n-1, straight from its
    edge list, in O(n + m): count each vertex's edges, turn the counts into starts, then drop each edge
    into the next free slot of its vertex's stretch."""
    start = [0] * (n + 1)
    for a, _ in edges:
        start[a + 1] += 1                       # count the edges leaving a
    for v in range(n):
        start[v + 1] += start[v]                # running totals: where each stretch begins
    nxt, targets = start[:n], [0] * len(edges)
    for a, b in edges:
        targets[nxt[a]] = b
        nxt[a] += 1
    return start, targets


def reverse_compressed(n: int, start: list[int], targets: list[int]) -> tuple[list[int], list[int]]:
    """The compressed form of the reverse graph: every edge a -> b becomes b -> a. O(n + m)."""
    return compressed_from_edges(n, [(b, a) for a in range(n) for b in targets[start[a]:start[a + 1]]])


def matrix_cells_read(n: int) -> int:
    """Thinking Problem 3: a search of the path 0-1-...-(n-1) stored as a matrix reads every row once."""
    return n * n


if __name__ == "__main__":
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 2)]
    print(compressed_from_edges(4, edges))
    print(reverse_compressed(4, *compressed_from_edges(4, edges)))
    print(matrix_cells_read(2000), 2 * (2000 - 1))
