"""Volume 5, Chapter 7 - Heapsort: A First Look at Heaps.

A max-heap stored in a list: the children of index i are 2i+1 and 2i+2; every parent >= its children.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import heapq


def sift_down(a: list, start: int, end: int) -> None:
    """Push a[start] down until both children are smaller (only looks at indexes < end)."""
    parent = start
    while True:
        largest = parent
        left, right = 2 * parent + 1, 2 * parent + 2
        if left < end and a[left] > a[largest]:
            largest = left
        if right < end and a[right] > a[largest]:
            largest = right
        if largest == parent:
            return
        a[parent], a[largest] = a[largest], a[parent]
        parent = largest


def build_max_heap(a: list) -> None:
    """Fix every parent from the last one up to the root. Surprisingly O(n), not O(n log n)."""
    for start in range(len(a) // 2 - 1, -1, -1):
        sift_down(a, start, len(a))


def is_max_heap(a: list) -> bool:
    return all(a[(i - 1) // 2] >= a[i] for i in range(1, len(a)))


def heapsort(a: list) -> None:
    """Build a max-heap, then repeatedly swap the root (the largest) to the end and shrink the heap.
    O(n log n) in every case, in place (O(1) extra space). Not stable."""
    build_max_heap(a)
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)


def top_k_largest(scores: list[int], k: int) -> list[int]:
    """Practical example: the k highest scores without sorting everything - a min-heap of size k (Python's heapq)."""
    heap: list[int] = []
    for s in scores:
        if len(heap) < k:
            heapq.heappush(heap, s)
        elif s > heap[0]:
            heapq.heapreplace(heap, s)       # drop the smallest of the current top k
    return sorted(heap, reverse=True)


def emergency_order(patients: list[tuple[int, str]]) -> list[str]:
    """Industry example: a hospital triage queue - most urgent first (higher number = more urgent)."""
    heap = [(-urgency, i, name) for i, (urgency, name) in enumerate(patients)]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[2] for _ in range(len(heap))]


if __name__ == "__main__":
    a = [4, 10, 3, 5, 1, 8]
    build_max_heap(a)
    print("max-heap:", a, is_max_heap(a))
    heapsort(a)
    print("heapsorted:", a)
    print("top 3:", top_k_largest([55, 91, 72, 88, 60, 99, 47], 3))
    print(emergency_order([(2, "sprained ankle"), (5, "chest pain"), (3, "deep cut"), (5, "allergic reaction")]))
