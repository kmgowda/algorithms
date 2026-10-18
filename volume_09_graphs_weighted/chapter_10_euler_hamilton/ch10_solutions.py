"""Volume 9, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

import itertools
from collections import Counter
from typing import Hashable

from ch10_examples import hierholzer


def undirected_euler_possible(edges: list[tuple[Hashable, Hashable]]) -> bool:
    """Exercise 1 (Konigsberg): an undirected connected graph has an Euler path iff 0 or 2 vertices have odd degree."""
    deg = Counter()
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    return sum(1 for d in deg.values() if d % 2) in (0, 2)


def de_bruijn(k: int, alphabet: str = "01") -> str:
    """Exercise 2 (LeetCode 753 idea): the shortest string containing every length-k code as a substring.
    Vertices = (k-1)-length strings; each length-k code is an edge; an Euler circuit spells the answer."""
    if k == 1:
        return alphabet
    nodes = ["".join(p) for p in itertools.product(alphabet, repeat=k - 1)]
    edges = [(n, n[1:] + ch) for n in nodes for ch in alphabet]
    path = hierholzer(edges)
    assert path is not None
    return path[0] + "".join(v[-1] for v in path[1:])


def brute_force_tour(dist: list[list[float]]) -> float:
    """Exercise 3: try every order of cities (n!) to check the Held-Karp answer."""
    n = len(dist)
    best = float("inf")
    for perm in itertools.permutations(range(1, n)):
        route = (0, *perm, 0)
        best = min(best, sum(dist[a][b] for a, b in zip(route, route[1:])))
    return best if n > 1 else 0.0


if __name__ == "__main__":
    bridges = [("N", "I"), ("N", "I"), ("S", "I"), ("S", "I"), ("N", "E"), ("S", "E"), ("I", "E")]
    print("Konigsberg walk possible:", undirected_euler_possible(bridges))
    print(de_bruijn(3), brute_force_tour([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]))
