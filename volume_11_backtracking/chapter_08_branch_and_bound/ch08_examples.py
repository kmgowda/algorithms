"""Volume 11, Chapter 8 - Branch-and-Bound: Assignment Problem, Travelling Salesperson, 0/1 Knapsack.

Branch-and-bound = backtracking for OPTIMIZATION: keep the best answer found so far, and prune any branch
whose optimistic BOUND can't beat it.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import heapq
import itertools
import math


def assignment_bnb(cost: list[list[float]]) -> tuple[float, list[int], int]:
    """Give worker i task perm[i], minimising total cost. Depth-first branch-and-bound.
    Bound = cost so far + for every unassigned worker, their cheapest still-free task (never overestimates).
    Returns (best cost, assignment, nodes)."""
    n = len(cost)
    best = [math.inf, []]
    nodes = 0
    taken = [False] * n
    perm: list[int] = []

    def bound(so_far: float) -> float:
        free = [t for t in range(n) if not taken[t]]
        return so_far + sum(min(cost[w][t] for t in free) for w in range(len(perm), n))

    def go(so_far: float) -> None:
        nonlocal nodes
        nodes += 1
        w = len(perm)
        if w == n:
            if so_far < best[0]:
                best[0], best[1] = so_far, list(perm)
            return
        for t in sorted(range(n), key=lambda t: cost[w][t]):        # cheapest first: good answers early
            if taken[t]:
                continue
            taken[t] = True
            perm.append(t)
            if bound(so_far + cost[w][t]) < best[0]:
                go(so_far + cost[w][t])
            perm.pop()
            taken[t] = False

    go(0.0)
    return best[0], best[1], nodes


def tsp_bnb(dist: list[list[float]]) -> tuple[float, list[int], int]:
    """Shortest round trip from city 0. Bound = length so far + for each city still to leave (the current one and
    every unvisited one), its cheapest edge to a city it could still go to. Returns (length, tour, nodes)."""
    n = len(dist)
    if n == 1:
        return 0.0, [0, 0], 1
    best = [math.inf, []]
    nodes = 0
    path, seen = [0], {0}

    def bound(length: float) -> float:
        remaining = [c for c in range(n) if c not in seen]
        targets = remaining + [0]
        est = length + min(dist[path[-1]][t] for t in remaining) if remaining else length
        for c in remaining:
            est += min(dist[c][t] for t in targets if t != c)
        return est

    def go(length: float) -> None:
        nonlocal nodes
        nodes += 1
        if len(path) == n:
            total = length + dist[path[-1]][0]
            if total < best[0]:
                best[0], best[1] = total, path + [0]
            return
        if bound(length) >= best[0]:
            return
        here = path[-1]
        for c in sorted((c for c in range(n) if c not in seen), key=lambda c: dist[here][c]):
            path.append(c)
            seen.add(c)
            go(length + dist[here][c])
            path.pop()
            seen.remove(c)

    go(0.0)
    return best[0], best[1], nodes


def tsp_brute(dist: list[list[float]]) -> tuple[float, int]:
    """Reference: every tour; returns (length, tours examined)."""
    n = len(dist)
    best, count = math.inf, 0
    for perm in itertools.permutations(range(1, n)):
        count += 1
        tour = (0, *perm, 0)
        best = min(best, sum(dist[a][b] for a, b in zip(tour, tour[1:])))
    return (best if n > 1 else 0.0), count


def knapsack_best_first(items: list[tuple[str, int, int]], capacity: int) -> tuple[int, list[str], int]:
    """0/1 knapsack, BEST-FIRST branch-and-bound: always expand the node with the highest optimistic bound.
    Bound = value so far + the FRACTIONAL knapsack of the rest (V10-C4) - an overestimate, so it's safe.
    Returns (best value, items taken, nodes expanded)."""
    order = sorted(items, key=lambda it: it[2] / it[1], reverse=True)

    def bound(i: int, weight: int, value: float) -> float:
        room = capacity - weight
        for _, w, v in order[i:]:
            if w <= room:
                room -= w
                value += v
            else:
                return value + v * room / w
        return value

    best_value, best_take = 0, []
    tie = itertools.count()
    heap = [(-bound(0, 0, 0), next(tie), 0, 0, 0, [])]
    nodes = 0
    while heap:
        neg_b, _, i, weight, value, take = heapq.heappop(heap)
        if -neg_b <= best_value:
            break                                   # nothing left can beat the best: done
        nodes += 1
        if i == len(order):
            continue
        name, w, v = order[i]
        if weight + w <= capacity:                  # branch 1: take item i
            nv = value + v
            if nv > best_value:
                best_value, best_take = nv, take + [name]
            heapq.heappush(heap, (-bound(i + 1, weight + w, nv), next(tie), i + 1, weight + w, nv, take + [name]))
        b = bound(i + 1, weight, value)             # branch 2: skip item i
        if b > best_value:
            heapq.heappush(heap, (-b, next(tie), i + 1, weight, value, take))
    return best_value, sorted(best_take), nodes


def crew_assignment(pilots: list[str], flights: list[str], hours: list[list[float]]) -> dict[str, str]:
    """Industry example: assign pilots to flights minimising total extra travel hours."""
    _, perm, _ = assignment_bnb(hours)
    return {pilots[i]: flights[t] for i, t in enumerate(perm)}


if __name__ == "__main__":
    cost = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
    print("assignment:", assignment_bnb(cost))
    rng_dist = [[0, 29, 20, 21, 16, 31, 100, 12], [29, 0, 15, 29, 28, 40, 72, 21], [20, 15, 0, 15, 14, 25, 81, 9],
                [21, 29, 15, 0, 4, 12, 92, 12], [16, 28, 14, 4, 0, 16, 94, 9], [31, 40, 25, 12, 16, 0, 95, 24],
                [100, 72, 81, 92, 94, 95, 0, 90], [12, 21, 9, 12, 9, 24, 90, 0]]
    length, tour, nodes = tsp_bnb(rng_dist)
    print("TSP branch-and-bound:", length, tour, nodes, "nodes | brute force:", tsp_brute(rng_dist))
    bag = [("tent", 5, 60), ("stove", 3, 50), ("food", 4, 70), ("camera", 2, 30), ("books", 3, 20), ("rope", 1, 15)]
    print("knapsack best-first:", knapsack_best_first(bag, 10))
    print(crew_assignment(["Ira", "Jo", "Kai"], ["BLR-DEL", "BOM-GOI", "MAA-CCU"], [[3, 1, 4], [2, 5, 1], [1, 2, 3]]))
