"""Volume 7, Chapter 3 - Heap Patterns: Top K, K-way Merge, Running Median.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import heapq
from typing import Iterable, Iterator


def top_k(values: Iterable[int], k: int) -> list[int]:
    """Pattern 1: keep a MIN-heap of the k largest seen so far; its root is the weakest of the top k. O(n log k)."""
    heap: list[int] = []
    for v in values:
        if len(heap) < k:
            heapq.heappush(heap, v)
        elif v > heap[0]:
            heapq.heapreplace(heap, v)
    return sorted(heap, reverse=True)


def k_way_merge(lists: list[list[int]]) -> list[int]:
    """Pattern 2: a heap holds the current front of each sorted list. O(N log k) for N items in k lists."""
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out


class RunningMedian:
    """Pattern 3 (LeetCode 295): two heaps - a max-heap for the smaller half, a min-heap for the larger half.
    Invariant: every value in `low` <= every value in `high`, and their sizes differ by at most 1."""

    def __init__(self) -> None:
        self.low: list[float] = []            # max-heap via negated values
        self.high: list[float] = []           # min-heap

    def add(self, value: float) -> None:
        heapq.heappush(self.low, -value)
        heapq.heappush(self.high, -heapq.heappop(self.low))      # move the largest of the low half up
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))  # rebalance sizes

    def median(self) -> float:
        if not self.low:
            raise ValueError("no values yet")
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2


def medians_of_stream(values: Iterable[float]) -> Iterator[float]:
    rm = RunningMedian()
    for v in values:
        rm.add(v)
        yield rm.median()


def k_closest_shops(shops: list[tuple[str, int, int]], k: int) -> list[str]:
    """Industry example (LeetCode 973): nearest k shops to (0, 0) with a size-k MAX-heap by distance."""
    heap: list[tuple[int, str]] = []
    for name, x, y in shops:
        d = x * x + y * y
        if len(heap) < k:
            heapq.heappush(heap, (-d, name))
        elif d < -heap[0][0]:
            heapq.heapreplace(heap, (-d, name))
    return [name for _, name in sorted(heap, reverse=True)]


if __name__ == "__main__":
    print(top_k([55, 91, 72, 88, 60, 99, 47], 3))
    print(k_way_merge([[1, 4, 9], [2, 3, 10], [0, 5]]))
    print(list(medians_of_stream([5, 15, 1, 3, 8])))
    print(k_closest_shops([("Bakery", 3, 4), ("Pharmacy", 1, 1), ("Bookshop", -2, 2), ("Florist", 6, 1)], 2))
