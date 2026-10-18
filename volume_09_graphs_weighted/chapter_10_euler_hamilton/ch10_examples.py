"""Volume 9, Chapter 10 - Eulerian and Hamiltonian Paths: Every Road Once vs. Every City Once.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

from collections import Counter
from typing import Hashable


def euler_start(edges: list[tuple[Hashable, Hashable]]) -> Hashable | None:
    """Directed: an Euler path exists only if at most one vertex has out - in = 1 (the start), at most one has
    in - out = 1 (the end), and all others are balanced (plus connectivity). Returns a valid start or None."""
    out, inn = Counter(u for u, _ in edges), Counter(v for _, v in edges)
    vertices = set(out) | set(inn)
    starts = [v for v in vertices if out[v] - inn[v] == 1]
    ends = [v for v in vertices if inn[v] - out[v] == 1]
    if any(abs(out[v] - inn[v]) > 1 for v in vertices) or len(starts) > 1 or len(ends) > 1 or len(starts) != len(ends):
        return None
    return starts[0] if starts else (min(vertices, key=str) if vertices else None)


def hierholzer(edges: list[tuple[Hashable, Hashable]]) -> list[Hashable] | None:
    """Hierholzer's algorithm: walk until stuck, then back up and splice in side loops. O(E).
    Returns the vertex sequence using every edge once, or None."""
    start = euler_start(edges)
    if start is None:
        return None
    adj: dict[Hashable, list[Hashable]] = {}
    for u, v in sorted(edges, key=lambda e: (str(e[0]), str(e[1])), reverse=True):
        adj.setdefault(u, []).append(v)               # reversed so pop() takes the smallest first
    stack, path = [start], []
    while stack:
        v = stack[-1]
        if adj.get(v):
            stack.append(adj[v].pop())
        else:
            path.append(stack.pop())
    path.reverse()
    return path if len(path) == len(edges) + 1 else None   # None if the edges weren't all connected


def itinerary(tickets: list[tuple[str, str]], home: str) -> list[str]:
    """Industry example (LeetCode 332): use every flight ticket once, starting from home; smallest order on ties."""
    adj: dict[str, list[str]] = {}
    for a, b in sorted(tickets, reverse=True):
        adj.setdefault(a, []).append(b)
    stack, route = [home], []
    while stack:
        while adj.get(stack[-1]):
            stack.append(adj[stack[-1]].pop())
        route.append(stack.pop())
    return route[::-1]


def hamiltonian_path_exists(n: int, edges: list[tuple[int, int]]) -> bool:
    """Visit every vertex exactly once (undirected). NP-hard in general; bitmask DP does it in O(2^n * n^2).
    reach[mask][v] = can a path visit exactly the set 'mask' and end at v?"""
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    reach = [0] * (1 << n)                           # reach[mask] = bitset of possible end vertices
    for v in range(n):
        reach[1 << v] |= 1 << v
    for mask in range(1 << n):
        ends = reach[mask]
        if not ends:
            continue
        for v in range(n):
            if ends >> v & 1:
                options = adj[v] & ~mask
                w = 0
                while options:
                    if options & 1:
                        reach[mask | (1 << w)] |= 1 << w
                    options >>= 1
                    w += 1
    return n == 0 or reach[(1 << n) - 1] != 0


def shortest_tour(dist: list[list[float]]) -> float:
    """Practical example: the travelling salesperson - the shortest round trip through every city (Held-Karp DP).
    best[mask][v] = shortest path from city 0 through 'mask', ending at v. O(2^n * n^2)."""
    n = len(dist)
    INF = float("inf")
    best = [[INF] * n for _ in range(1 << n)]
    best[1][0] = 0.0
    for mask in range(1 << n):
        for v in range(n):
            if best[mask][v] == INF:
                continue
            for w in range(n):
                if not mask >> w & 1:
                    nm = mask | (1 << w)
                    best[nm][w] = min(best[nm][w], best[mask][v] + dist[v][w])
    full = (1 << n) - 1
    return min(best[full][v] + dist[v][0] for v in range(n)) if n > 1 else 0.0


if __name__ == "__main__":
    print("Euler path:", hierholzer([("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")]))
    print("itinerary:", itinerary([("MUC", "LHR"), ("JFK", "MUC"), ("SFO", "SJC"), ("LHR", "SFO")], "JFK"))
    print("Hamiltonian path on a 4-cycle:", hamiltonian_path_exists(4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
          "| on a star:", hamiltonian_path_exists(4, [(0, 1), (0, 2), (0, 3)]))
    d = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    print("shortest delivery round trip:", shortest_tour(d))
