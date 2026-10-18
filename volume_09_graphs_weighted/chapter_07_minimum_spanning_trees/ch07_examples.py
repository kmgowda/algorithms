"""Volume 9, Chapter 7 - Minimum Spanning Trees: Kruskal and Prim.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import heapq
import itertools
import math
from typing import Hashable

Edge = tuple[float, Hashable, Hashable]          # (weight, u, v) - weight first so edges sort by cost


class DSU:
    """Union-find with path halving and union by size (V7-C5)."""

    def __init__(self, items) -> None:
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x: Hashable) -> Hashable:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: Hashable, b: Hashable) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def kruskal(vertices: list[Hashable], edges: list[Edge]) -> tuple[float, list[Edge]]:
    """Take edges cheapest first; keep an edge unless it would close a loop (union-find says 'already joined').
    O(E log E). Returns (total cost, chosen edges). A forest if the graph is disconnected."""
    dsu = DSU(vertices)
    chosen: list[Edge] = []
    for w, u, v in sorted(edges, key=lambda e: e[0]):
        if dsu.union(u, v):
            chosen.append((w, u, v))
            if len(chosen) == len(vertices) - 1:
                break
    return sum(w for w, _, _ in chosen), chosen


def prim(graph: dict[Hashable, dict[Hashable, float]], start: Hashable) -> tuple[float, list[Edge]]:
    """Grow one tree from start: always add the cheapest edge leaving the tree (a heap of candidate edges).
    O(E log V). Like Dijkstra, but the key is the edge weight, not the distance from the start."""
    in_tree = {start}
    tie = itertools.count()
    heap = [(w, next(tie), start, v) for v, w in graph[start].items()]
    heapq.heapify(heap)
    chosen: list[Edge] = []
    while heap and len(in_tree) < len(graph):
        w, _, u, v = heapq.heappop(heap)
        if v in in_tree:
            continue
        in_tree.add(v)
        chosen.append((w, u, v))
        for x, wx in graph[v].items():
            if x not in in_tree:
                heapq.heappush(heap, (wx, next(tie), v, x))
    return sum(w for w, _, _ in chosen), chosen


def connect_points(points: list[tuple[int, int]]) -> int:
    """Industry example (LeetCode 1584): cheapest cabling joining every building, cost = Manhattan distance.
    Dense graph (every pair), so array-based Prim in O(V^2) beats building all V^2 edges for Kruskal."""
    n = len(points)
    best = [math.inf] * n
    best[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=lambda i: best[i])
        used[u] = True
        total += best[u]
        for v in range(n):
            if not used[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if d < best[v]:
                    best[v] = d
    return int(total)


def clusters(points: dict[str, tuple[float, float]], k: int) -> list[list[str]]:
    """Industry example: single-linkage clustering - run Kruskal but stop when k groups remain."""
    names = list(points)
    edges = [(math.dist(points[a], points[b]), a, b) for a, b in itertools.combinations(names, 2)]
    dsu, groups = DSU(names), len(names)
    for w, a, b in sorted(edges):
        if groups == k:
            break
        if dsu.union(a, b):
            groups -= 1
    out: dict[Hashable, list[str]] = {}
    for n in names:
        out.setdefault(dsu.find(n), []).append(n)
    return sorted(sorted(g) for g in out.values())


if __name__ == "__main__":
    towns = ["A", "B", "C", "D", "E"]
    cables = [(4, "A", "B"), (1, "A", "C"), (3, "B", "C"), (2, "B", "D"), (5, "C", "D"), (7, "D", "E"), (6, "C", "E")]
    print("Kruskal:", kruskal(towns, cables))
    g: dict[Hashable, dict[Hashable, float]] = {t: {} for t in towns}
    for w, u, v in cables:
        g[u][v] = g[v][u] = w
    print("Prim:   ", prim(g, "A"))
    print("cabling buildings:", connect_points([(0, 0), (2, 2), (3, 10), (5, 2), (7, 0)]))
    print("clusters:", clusters({"lion": (0, 0), "tiger": (1, 0), "zebra": (10, 10), "horse": (11, 10), "eagle": (5, 20)}, 3))
