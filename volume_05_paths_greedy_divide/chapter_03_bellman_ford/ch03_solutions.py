"""Volume 5, Chapter 3 - Thinking Problems: costs that fall for ever (Thinking Problem 2), and the one-round
breadth-first order that does not work (Thinking Problem 3).

Run:  python3 ch03_solutions.py
"""

from __future__ import annotations

from collections import deque


def costs_with_minus_infinity(vertices: list, edges: list, start) -> dict:
    """Cheapest cost from start to every vertex: a number, float('inf') if unreachable, or float('-inf') if a
    negative cycle on the way makes it as cheap as you like. V - 1 rounds, one more to find the vertices still
    improving, then a breadth-first walk marks everything downstream of them."""
    inf = float("inf")
    dist = {v: inf for v in vertices}
    dist[start] = 0
    for _ in range(len(vertices) - 1):
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
    out = {v: [] for v in vertices}
    for a, b, _ in edges:
        out[a].append(b)
    falling = deque(b for a, b, w in edges if dist[a] + w < dist[b])
    seen = set(falling)
    while falling:
        v = falling.popleft()
        dist[v] = -inf
        for w in out[v]:
            if w not in seen:
                seen.add(w)
                falling.append(w)
    return dist


def one_round_in_bfs_order(vertices: list, edges: list, start) -> dict:
    """The WRONG shortcut: one single round, relaxing the legs out of each vertex in breadth-first order."""
    out = {v: [] for v in vertices}
    for a, b, w in edges:
        out[a].append((b, w))
    order, seen, queue = [], {start}, deque([start])
    while queue:
        v = queue.popleft()
        order.append(v)
        for b, _ in out[v]:
            if b not in seen:
                seen.add(b)
                queue.append(b)
    dist = {v: float("inf") for v in vertices}
    dist[start] = 0
    for a in order:
        for b, w in out[a]:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
    return dist


if __name__ == "__main__":
    import ch03_examples as ex
    print(one_round_in_bfs_order(ex.DEPOTS, ex.LEGS, "A"))
    print(costs_with_minus_infinity(ex.DEPOTS + ["F", "G"], ex.LEGS + [("B", "F", 1), ("F", "G", -2), ("G", "F", 1)],
                                    "A"))
