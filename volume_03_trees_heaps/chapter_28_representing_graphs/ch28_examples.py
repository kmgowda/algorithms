"""Volume 3, Chapter 22 - Representing Graphs.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

import random
import time

BRANCHES = ["Central", "North", "East", "South", "West", "Harbour"]
ROUTES = [("Central", "North"), ("Central", "East"), ("Central", "South"), ("Central", "West"),
          ("North", "East"), ("South", "Harbour"), ("West", "Harbour")]


def adjacency_matrix(vertices: list, edges: list) -> list[list[int]]:
    """matrix[i][j] = 1 when vertices i and j are joined (Figure 22.2)."""
    index = {v: i for i, v in enumerate(vertices)}
    m = [[0] * len(vertices) for _ in vertices]
    for a, b in edges:
        m[index[a]][index[b]] = m[index[b]][index[a]] = 1
    return m


def adjacency_list(vertices: list, edges: list) -> dict:
    """Each vertex keeps the list of its neighbours (Figure 22.3)."""
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def compressed(vertices: list, edges: list) -> tuple[list[int], list]:
    """Pack the adjacency lists into two arrays (Section 22.6): vertex i's neighbours are
    targets[start[i]:start[i + 1]]. start has n + 1 entries; targets has one entry per list entry."""
    adj = adjacency_list(vertices, edges)
    start, targets = [0], []
    for v in vertices:
        targets.extend(adj[v])
        start.append(len(targets))
    return start, targets


def compressed_neighbours(vertices: list, start: list[int], targets: list, v) -> list:
    i = vertices.index(v)
    return targets[start[i]:start[i + 1]]


def weighted_adjacency(edges: list[tuple]) -> dict:
    """Directed, weighted: adj[a][b] = minutes from a to b."""
    adj: dict = {}
    for a, b, w in edges:
        adj.setdefault(a, {})[b] = w
        adj.setdefault(b, {})
    return adj


def degrees(adj: dict) -> dict:
    return {v: len(ns) for v, ns in adj.items()}


def grid_neighbours(grid: list[str], r: int, c: int) -> list[tuple[int, int]]:
    """An implicit graph: open squares of a grid, joined to open squares beside them (Volume 2, Chapter 20)."""
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]) and grid[rr][cc] == ".":
            out.append((rr, cc))
    return out


def experiment(n: int = 2000, m: int = 6000, queries: int = 20000, seed: int = 1) -> dict:
    """Build both representations of a sparse random graph and time two kinds of question."""
    rng = random.Random(seed)
    edges = set()
    while len(edges) < m:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    matrix = [bytearray(n) for _ in range(n)]
    adj = [[] for _ in range(n)]
    adj_sets = [set() for _ in range(n)]
    for a, b in edges:
        matrix[a][b] = matrix[b][a] = 1
        adj[a].append(b)
        adj[b].append(a)
        adj_sets[a].add(b)
        adj_sets[b].add(a)
    pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(queries)]
    vs = [rng.randrange(n) for _ in range(queries)]
    out = {"matrix cells": n * n, "list entries": 2 * m}
    t = time.perf_counter(); sum(matrix[a][b] for a, b in pairs); out["edge? matrix ms"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); sum(b in adj[a] for a, b in pairs); out["edge? list ms"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); sum(b in adj_sets[a] for a, b in pairs); out["edge? set ms"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter()
    for v in vs:
        row = matrix[v]
        sum(1 for u in range(n) if row[u])
    out["neighbours matrix ms"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter()
    for v in vs:
        sum(1 for _ in adj[v])
    out["neighbours list ms"] = (time.perf_counter() - t) * 1e3
    return out


if __name__ == "__main__":
    m = adjacency_matrix(BRANCHES, ROUTES)
    for name, row in zip(BRANCHES, m):
        print(f"{name:8s}", row)
    print(adjacency_list(BRANCHES, ROUTES))
    print(degrees(adjacency_list(BRANCHES, ROUTES)), sum(map(sum, m)))
    for k, v in experiment().items():
        print(f"{k:22s} {v:,.1f}" if isinstance(v, float) else f"{k:22s} {v:,}")
