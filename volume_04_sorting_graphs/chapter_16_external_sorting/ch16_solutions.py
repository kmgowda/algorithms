"""Volume 4, Chapter 16 - Thinking Problems: model solutions.

Thinking Problem 2: the cheapest order in which to merge sorted runs of unequal lengths, two at a time.

Run:  python3 ch16_solutions.py
"""

from __future__ import annotations

import heapq


def cheapest_merge_order(lengths: list[int]) -> tuple[int, list[tuple[int, int]]]:
    """Merging two runs of lengths a and b copies a + b items. Always merge the two shortest runs
    (Thinking Problem 13.2). Returns (total items copied, the merges as (a, b) pairs in order)."""
    heap = list(lengths)
    heapq.heapify(heap)
    total, merges = 0, []
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        merges.append((a, b))
        total += a + b
        heapq.heappush(heap, a + b)
    return total, merges


def merge_cost_in_order(lengths: list[int]) -> int:
    """The cost of merging the runs left to right: ((r1 + r2) + r3) + ..., for comparison."""
    total, acc = 0, (lengths[0] if lengths else 0)
    for x in lengths[1:]:
        acc += x
        total += acc
    return total


def cheapest_by_brute_force(lengths: list[int]) -> int:
    """The true minimum over every merge order (exponential; for checking small cases only)."""
    if len(lengths) <= 1:
        return 0
    best = None
    for i in range(len(lengths)):
        for j in range(i + 1, len(lengths)):
            rest = [x for k, x in enumerate(lengths) if k not in (i, j)] + [lengths[i] + lengths[j]]
            cost = lengths[i] + lengths[j] + cheapest_by_brute_force(rest)
            best = cost if best is None else min(best, cost)
    return best


if __name__ == "__main__":
    runs = [20, 30, 10, 5, 30]
    print(cheapest_merge_order(runs), merge_cost_in_order(runs))
