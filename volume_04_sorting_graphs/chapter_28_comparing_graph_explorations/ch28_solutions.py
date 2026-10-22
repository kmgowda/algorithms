"""Volume 4, Chapter 28 - Thinking Problems: model solutions.

Run:  python3 ch28_solutions.py
"""

from __future__ import annotations

from collections import deque


def girth(adj: dict) -> int | None:
    """Thinking Problem 2: the length of the shortest cycle of a simple undirected graph (no self-loops, no
    parallel roads), or None for a forest. One BFS from every place; each non-tree road x-y closes a cycle of at
    most dist[x] + dist[y] + 1 roads, and from a place on a shortest cycle some road gives exactly its length.
    Cost O(V * (V + E))."""
    best = None
    for s in adj:
        dist, parent, q = {s: 0}, {s: None}, deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in dist:
                    dist[y], parent[y] = dist[x] + 1, x
                    q.append(y)
                elif y != parent[x]:                  # a non-tree road closes a cycle
                    length = dist[x] + dist[y] + 1
                    best = length if best is None else min(best, length)
    return best


def back_road_count(adj: dict) -> int:
    """Thinking Problem 1: every search leaves E - V + c roads off its forest (c = number of pieces)."""
    roads = sum(len(n) for n in adj.values()) // 2
    seen, pieces = set(), 0
    for s in adj:
        if s not in seen:
            pieces += 1
            seen.add(s)
            stack = [s]
            while stack:
                v = stack.pop()
                for w in adj[v]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
    return roads - len(adj) + pieces


def has_cycle_seen_test(g: dict) -> bool:
    """Thinking Problem 3, the FLAWED method: the undirected test 'an arrow to an already visited vertex means a
    cycle', carried over to a directed graph. It reports cycles that are not there."""
    seen = set()

    def visit(v):
        seen.add(v)
        for w in g[v]:
            if w in seen or visit(w):
                return True
        return False
    return any(visit(s) for s in g if s not in seen)


if __name__ == "__main__":
    import ch28_examples as ex
    print(girth(ex.bfs_m.adjacency()), back_road_count(ex.bfs_m.adjacency()))
    print(has_cycle_seen_test({"A": ["B", "C"], "B": [], "C": ["B"]}))
