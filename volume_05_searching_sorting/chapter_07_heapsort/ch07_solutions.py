"""Volume 5, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

import heapq

from ch07_examples import build_max_heap, sift_down


def kth_largest(values: list[int], k: int) -> int:
    """Exercise 1 (LeetCode 215): keep a min-heap of the k largest; its root is the answer. O(n log k)."""
    heap = values[:k]
    heapq.heapify(heap)
    for v in values[k:]:
        if v > heap[0]:
            heapq.heapreplace(heap, v)
    return heap[0]


def last_stone(stones: list[int]) -> int:
    """Exercise 2 (LeetCode 1046): smash the two heaviest; the difference returns. Max-heap via negatives."""
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = -heapq.heappop(heap), -heapq.heappop(heap)
        if a != b:
            heapq.heappush(heap, -(a - b))
    return -heap[0] if heap else 0


def heap_children(a: list, i: int) -> list:
    """Exercise 3: the children of index i in a list-stored heap."""
    return [a[c] for c in (2 * i + 1, 2 * i + 2) if c < len(a)]


def heapsort_steps(values: list[int]) -> list[list[int]]:
    """Exercise 4: snapshots after building the heap and after each extraction, for tracing by hand."""
    a = list(values)
    build_max_heap(a)
    steps = [list(a)]
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)
        steps.append(list(a))
    return steps


if __name__ == "__main__":
    print(kth_largest([3, 2, 1, 5, 6, 4], 2), last_stone([2, 7, 4, 1, 8, 1]), heap_children([10, 5, 8, 4, 1], 1))
    for s in heapsort_steps([4, 10, 3, 5]):
        print(s)
