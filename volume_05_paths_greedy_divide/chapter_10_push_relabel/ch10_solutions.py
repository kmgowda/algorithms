"""Volume 5, Chapter 10 - model solutions to the Thinking Problems (Section 10.15).

Run:  python3 ch10_solutions.py
"""

from __future__ import annotations

from collections import deque

import ch10_examples as ex


def push_relabel_gap(nodes: list, edges: list, s, t) -> tuple[int, int, int]:
    """Thinking Problem 2: FIFO push-relabel with the gap rule. When a relabel leaves no place at some height k
    with 0 < k < n, every place standing between k and n can no longer reach t, so it is lifted straight to n + 1.
    Returns (total flow, pushes, relabels); a gap lift counts as one relabel per place lifted."""
    n = len(nodes)
    room, adj = ex.residual_room(nodes, edges)
    height = {v: 0 for v in nodes}
    height[s] = n
    level = [0] * (2 * n + 1)                          # level[k]: places other than s at height k
    level[0] = n - 1
    excess = {v: 0 for v in nodes}
    log = []
    active = ex.flood(s, t, room, adj, excess, log)
    pushes, relabels = len(log), 0
    while active:
        u = active.popleft()
        while excess[u] > 0:
            for v in adj[u]:
                if room[(u, v)] > 0 and height[u] == height[v] + 1:
                    amount = min(excess[u], room[(u, v)])
                    room[(u, v)] -= amount
                    room[(v, u)] += amount
                    excess[u] -= amount
                    excess[v] += amount
                    pushes += 1
                    if v not in (s, t) and excess[v] == amount:
                        active.append(v)
                    if excess[u] == 0:
                        break
            if excess[u] == 0:
                break
            old = height[u]
            new = 1 + min(height[v] for v in adj[u] if room[(u, v)] > 0)
            level[old] -= 1
            height[u] = new
            level[new] += 1
            relabels += 1
            if 0 < old < n and level[old] == 0:          # a gap at height old
                for v in nodes:
                    if v != s and old < height[v] < n + 1:
                        level[height[v]] -= 1
                        height[v] = n + 1
                        level[n + 1] += 1
                        relabels += 1
    return excess[t], pushes, relabels


def push_relabel_low_source(nodes: list, edges: list, s, t) -> int:
    """Thinking Problem 3: the bug. The source is left at height 0 instead of n, so the first relabel of each place
    lets it push its excess straight back to the source. Returns the (wrong) total that reaches t."""
    room, adj = ex.residual_room(nodes, edges)
    height = {v: 0 for v in nodes}                     # BUG: height[s] should be len(nodes)
    excess = {v: 0 for v in nodes}
    active = ex.flood(s, t, room, adj, excess, None)
    while active:
        ex.discharge(active.popleft(), s, t, room, adj, height, excess, active, None)
    return excess[t]


if __name__ == "__main__":
    print(push_relabel_gap(ex.NODES, ex.PIPES, "Warehouse", "Library"))
    print(push_relabel_low_source(ex.NODES, ex.PIPES, "Warehouse", "Library"))
    for L, W in [(3, 3), (8, 8), (10, 12)]:
        nodes, edges = ex.layered_network(L, W)
        print(L, W, push_relabel_gap(nodes, edges, "s", "t"))
