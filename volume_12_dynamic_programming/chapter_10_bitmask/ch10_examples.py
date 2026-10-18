"""Volume 12, Chapter 10 - DP With Bitmasks: The Travelling Salesperson and Assignment.

A set of up to ~20 items fits in one integer: bit i is 1 when item i is in the set.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

from collections import deque


def set_to_mask(items: list[int]) -> int:
    mask = 0
    for i in items:
        mask |= 1 << i
    return mask


def mask_to_set(mask: int) -> list[int]:
    return [i for i in range(mask.bit_length()) if mask >> i & 1]


def held_karp(dist: list[list[float]]) -> tuple[float, list[int]]:
    """Shortest round trip from city 0 through every city (V9-C10), now with the route.
    best[mask][v] = shortest path starting at 0, visiting exactly the cities in mask, ending at v."""
    n = len(dist)
    if n == 1:
        return 0.0, [0, 0]
    INF = float("inf")
    full = (1 << n) - 1
    best = [[INF] * n for _ in range(1 << n)]
    prev = [[-1] * n for _ in range(1 << n)]
    best[1][0] = 0.0
    for mask in range(1 << n):
        if not mask & 1:
            continue                                      # every path starts at city 0
        for v in range(n):
            if best[mask][v] == INF:
                continue
            for w in range(n):
                if mask >> w & 1:
                    continue
                nm = mask | (1 << w)
                if best[mask][v] + dist[v][w] < best[nm][w]:
                    best[nm][w] = best[mask][v] + dist[v][w]
                    prev[nm][w] = v
    end = min(range(1, n), key=lambda v: best[full][v] + dist[v][0])
    total = best[full][end] + dist[end][0]
    route, mask, v = [], full, end
    while v != -1:
        route.append(v)
        mask, v = mask ^ (1 << v), prev[mask][v]
    return total, route[::-1] + [0]                    # the walk back ends at city 0


def assignment_bitmask(cost: list[list[int]]) -> int:
    """Worker k (k = number of tasks already used) picks any free task. best[mask] = cheapest way to fill those tasks."""
    n = len(cost)
    INF = float("inf")
    best = [INF] * (1 << n)
    best[0] = 0
    for mask in range(1 << n):
        k = bin(mask).count("1")
        if k == n or best[mask] == INF:
            continue
        for t in range(n):
            if not mask >> t & 1:
                best[mask | 1 << t] = min(best[mask | 1 << t], best[mask] + cost[k][t])
    return int(best[(1 << n) - 1])


def visit_all_nodes(adj: list[list[int]]) -> int:
    """LeetCode 847: shortest walk visiting every node (start anywhere, revisits allowed).
    BFS over states (node, visited-mask): the bitmask makes 'which nodes have I seen?' part of the state."""
    n = len(adj)
    full = (1 << n) - 1
    q = deque((v, 1 << v, 0) for v in range(n))
    seen = {(v, 1 << v) for v in range(n)}
    while q:
        v, mask, d = q.popleft()
        if mask == full:
            return d
        for w in adj[v]:
            state = (w, mask | 1 << w)
            if state not in seen:
                seen.add(state)
                q.append((w, mask | 1 << w, d + 1))
    return -1


def minimum_team(required: list[str], people: dict[str, list[str]]) -> list[str]:
    """Industry example (LeetCode 1125): the smallest team covering every required skill.
    best[skill-mask] = smallest team reaching exactly that coverage."""
    index = {s: i for i, s in enumerate(required)}
    full = (1 << len(required)) - 1
    best: dict[int, list[str]] = {0: []}
    for person, skills in people.items():
        pm = set_to_mask([index[s] for s in skills if s in index])
        for mask, team in list(best.items()):
            nm = mask | pm
            if nm not in best or len(best[nm]) > len(team) + 1:
                best[nm] = team + [person]
    return sorted(best.get(full, []))


if __name__ == "__main__":
    print(set_to_mask([0, 2, 3]), bin(13), mask_to_set(13))
    d = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    print("Held-Karp:", held_karp(d))
    print("assignment:", assignment_bitmask([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]))
    print("visit all nodes:", visit_all_nodes([[1, 2, 3], [0], [0], [0]]))
    team = minimum_team(["python", "sql", "design", "ml"],
                        {"Asha": ["python", "ml"], "Ben": ["sql"], "Cy": ["design", "sql"], "Dev": ["python"]})
    print("smallest team:", team)
