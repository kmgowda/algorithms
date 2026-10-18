"""Volume 8, Chapter 11 - The Big Comparison: DFS vs. BFS; Matrix vs. List; Union-Find vs. DFS.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import random
import timeit
from collections import deque


def random_edges(n: int, m: int, seed: int = 0) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    return [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]


def to_list(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def to_matrix(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    m = [[0] * n for _ in range(n)]
    for a, b in edges:
        m[a][b] = m[b][a] = 1
    return m


def dfs_order(adj: list[list[int]], s: int) -> list[int]:
    seen, order, stack = {s}, [], [s]
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return order


def bfs_order(adj: list[list[int]], s: int) -> list[int]:
    seen, order, queue = {s}, [], deque([s])
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return order


def bfs_matrix(m: list[list[int]], s: int) -> list[int]:
    """BFS on a matrix must scan a whole row per vertex: O(V^2) regardless of how few edges exist."""
    n = len(m)
    seen, order, queue = {s}, [], deque([s])
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in range(n):
            if m[v][w] and w not in seen:
                seen.add(w)
                queue.append(w)
    return order


def peak_frontier(adj: list[list[int]], s: int) -> dict[str, int]:
    """Memory comparison: the largest stack (DFS) vs. the largest queue (BFS) during a full search."""
    seen, stack, best_stack = {s}, [iter(adj[s])], 1      # recursion-style DFS: one iterator per open vertex
    while stack:
        w = next(stack[-1], None)
        if w is None:
            stack.pop()
        elif w not in seen:
            seen.add(w)
            stack.append(iter(adj[w]))
            best_stack = max(best_stack, len(stack))
    seen, queue, best_queue = {s}, deque([s]), 1
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
        best_queue = max(best_queue, len(queue))
    return {"DFS stack": best_stack, "BFS queue": best_queue}


def race_representations(n: int, m: int) -> dict[str, float]:
    edges = random_edges(n, m)
    adj, mat = to_list(n, edges), to_matrix(n, edges)
    return {
        "BFS on adjacency list": min(timeit.repeat(lambda: bfs_order(adj, 0), number=1, repeat=3)),
        "BFS on matrix": min(timeit.repeat(lambda: bfs_matrix(mat, 0), number=1, repeat=3)),
    }


def connectivity_queries(n: int, edges: list[tuple[int, int]], queries: list[tuple[int, int]]) -> tuple[list[bool], float, float]:
    """Many 'connected?' questions on a fixed graph: label components once (DFS) vs. union-find."""
    def with_labels() -> list[bool]:
        adj, label, comp = to_list(n, edges), [-1] * n, 0
        for s in range(n):
            if label[s] == -1:
                for v in dfs_order(adj, s):
                    label[v] = comp
                comp += 1
        return [label[a] == label[b] for a, b in queries]

    def with_union_find() -> list[bool]:
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for a, b in edges:
            parent[find(a)] = find(b)
        return [find(a) == find(b) for a, b in queries]

    t1 = min(timeit.repeat(with_labels, number=1, repeat=3))
    t2 = min(timeit.repeat(with_union_find, number=1, repeat=3))
    answers = with_labels()
    assert answers == with_union_find()
    return answers, t1, t2


def choose(task: str) -> str:
    return {
        "fewest hops": "BFS",
        "any path, or explore everything": "DFS (or BFS)",
        "cycles, topological order": "DFS (or Kahn's BFS-like algorithm)",
        "strongly connected components": "DFS (Kosaraju or Tarjan)",
        "bridges and cut vertices": "DFS with low-links",
        "two-sided split": "BFS 2-colouring",
        "connected? as edges keep arriving": "union-find",
        "connected? on a fixed graph, many queries": "label components once with DFS/BFS",
        "sparse graph storage": "adjacency list",
        "dense graph or constant-time edge checks": "adjacency matrix",
    }[task]


if __name__ == "__main__":
    adj = to_list(8, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7)])
    print("DFS:", dfs_order(adj, 0), "| BFS:", bfs_order(adj, 0))
    star = to_list(1001, [(0, i) for i in range(1, 1001)])
    chain = to_list(1001, [(i, i + 1) for i in range(1000)])
    print("star frontier:", peak_frontier(star, 0), "| chain frontier:", peak_frontier(chain, 0))
    print({k: round(v, 4) for k, v in race_representations(2000, 6000).items()})
    edges = random_edges(5000, 4000, seed=1)
    qs = [(i, (i * 37) % 5000) for i in range(5000)]
    _, t_label, t_uf = connectivity_queries(5000, edges, qs)
    print(f"labels {t_label:.4f}s vs union-find {t_uf:.4f}s")
    print(choose("fewest hops"))
