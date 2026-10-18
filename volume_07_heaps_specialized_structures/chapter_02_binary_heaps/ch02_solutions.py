"""Volume 7, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

import heapq

from ch02_examples import MinHeap, heapify


def is_min_heap(values: list) -> bool:
    """Exercise 1: every parent <= its children."""
    return all(values[(i - 1) // 2] <= values[i] for i in range(1, len(values)))


def heapify_swaps(values: list) -> int:
    """Exercise 2: count the swaps bottom-up heapify makes - always fewer than n."""
    a, n, swaps = list(values), len(values), 0
    for start in range(n // 2 - 1, -1, -1):
        i = start
        while True:
            smallest, left, right = i, 2 * i + 1, 2 * i + 2
            if left < n and a[left] < a[smallest]:
                smallest = left
            if right < n and a[right] < a[smallest]:
                smallest = right
            if smallest == i:
                break
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
            i = smallest
    return swaps


def heap_sort_with_heap(values: list[int]) -> list[int]:
    """Exercise 3: n pushes then n pops give sorted order (ties broken by position)."""
    h = MinHeap()
    for i, v in enumerate(values):
        h.push(i, v)
    return [h.pop()[1] for _ in range(len(h))]


def kth_smallest_via_heapify(values: list[int], k: int) -> int:
    """Exercise 4: heapify in O(n), then pop k times: O(n + k log n)."""
    a = heapify(values)
    for _ in range(k - 1):
        heapq.heappop(a)
    return a[0]


if __name__ == "__main__":
    print(is_min_heap([1, 3, 2, 7, 4]), heapify_swaps(list(range(100, 0, -1))), heap_sort_with_heap([5, 1, 4, 1]),
          kth_smallest_via_heapify([7, 2, 9, 4, 1], 3))
