"""Volume 11, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

import itertools
import math

from ch08_examples import assignment_bnb


def assignment_brute_nodes(cost: list[list[float]]) -> tuple[float, int]:
    """Exercise 1: brute force for comparison - (best cost, complete assignments examined = n!)."""
    n = len(cost)
    best, count = math.inf, 0
    for perm in itertools.permutations(range(n)):
        count += 1
        best = min(best, sum(cost[i][perm[i]] for i in range(n)))
    return best, count


def max_profit_assignment(profit: list[list[float]]) -> tuple[float, list[int]]:
    """Exercise 2: MAXIMISE profit by minimising negated profit with the same solver."""
    best, perm, _ = assignment_bnb([[-p for p in row] for row in profit])
    return -best, perm


def knapsack_dfs_bnb(items: list[tuple[int, int]], capacity: int) -> int:
    """Exercise 3: depth-first branch-and-bound knapsack (values, weights as (weight, value)) with the fractional bound."""
    order = sorted(items, key=lambda it: it[1] / it[0], reverse=True)
    best = 0

    def bound(i: int, room: int, value: float) -> float:
        for w, v in order[i:]:
            if w <= room:
                room -= w
                value += v
            else:
                return value + v * room / w
        return value

    def go(i: int, room: int, value: int) -> None:
        nonlocal best
        best = max(best, value)
        if i == len(order) or bound(i, room, value) <= best:
            return
        w, v = order[i]
        if w <= room:
            go(i + 1, room - w, value + v)
        go(i + 1, room, value)

    go(0, capacity, 0)
    return best


if __name__ == "__main__":
    cost = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
    print(assignment_brute_nodes(cost), max_profit_assignment([[3, 1], [1, 3]]), knapsack_dfs_bnb([(5, 60), (3, 50), (4, 70)], 8))
