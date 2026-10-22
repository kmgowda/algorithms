"""Volume 7, Chapter 28 - Thinking Problems.

Problem 1: the branching search for a cover of size k makes at most 2^(k + 1) - 1 calls (checked).
Problem 2: a largest independent set of a forest in O(n): repeatedly take a leaf (or a lone place) and drop its neighbour.
Problem 3: meet in the middle without sorting compares every pair of half-sums: 2^n work, no saving.
"""

from __future__ import annotations

import itertools


def forest_independent_set(vertices: list, edges: list) -> list:
    """Take any place with at most one remaining neighbour; delete it and that neighbour. Exact for forests."""
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    alive, chosen = set(vertices), []
    stack = [v for v in vertices if len(adj[v]) <= 1]
    while stack:
        v = stack.pop()
        if v not in alive or len(adj[v] & alive) > 1:
            continue
        chosen.append(v)
        gone = {v} | (adj[v] & alive)
        alive -= gone
        for u in gone:
            for w in adj[u] & alive:
                if len(adj[w] & alive) <= 1:
                    stack.append(w)
    return sorted(chosen, key=vertices.index)


def mitm_unsorted(values: list, target: int) -> tuple[bool, int]:
    """Half-sums compared pair by pair. Returns (found, pairs compared)."""
    half = len(values) // 2
    sums = lambda vs: [sum(c) for k in range(len(vs) + 1) for c in itertools.combinations(vs, k)]
    ls, rs = sums(values[:half]), sums(values[half:])
    pairs = 0
    for s in ls:
        for r in rs:
            pairs += 1
            if s + r == target:
                return True, pairs
    return False, pairs


if __name__ == "__main__":
    print(forest_independent_set(list("abcdefg"), [("a", "b"), ("b", "c"), ("c", "d"), ("b", "e"), ("f", "g")]))
    print(mitm_unsorted(list(range(1, 17)), 10 ** 6))
