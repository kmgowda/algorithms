"""Volume 4, Chapter 8 - Heapsort: model solutions to the Thinking Problems (Section 8.14).

Run:  python3 ch08_solutions.py
"""

from __future__ import annotations

import heapq

from ch08_examples import sift_down


def sort_nearly_sorted(a: list, k: int, counter: dict | None = None) -> list:
    """Thinking Problem 2: sort a list in which every item is at most k places from its sorted place, in
    O(n log k). A min-heap holds a window of k + 1 items; its smallest is always the next item of the output."""
    if k < 0:
        raise ValueError("k must be at least 0")
    heap, out = [], []
    for x in a:
        heapq.heappush(heap, x)
        if counter is not None:
            counter["max_heap_size"] = max(counter.get("max_heap_size", 0), len(heap))
        if len(heap) > k:                         # the window is full: its smallest item is final
            out.append(heapq.heappop(heap))
    while heap:
        out.append(heapq.heappop(heap))
    return out


def max_displacement(a: list) -> int:
    """How far the furthest item stands from its place in the sorted order (ties matched stably)."""
    order = sorted(range(len(a)), key=lambda p: a[p])
    return max((abs(p - q) for q, p in enumerate(order)), default=0)


def heapsort_top_down_build(a: list) -> list:
    """Thinking Problem 3: the slip of sifting the parents in the wrong order (position 0 first)."""
    a, n = list(a), len(a)
    for i in range(0, n // 2):                    # the bug: should run from n // 2 - 1 down to 0
        sift_down(a, i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)
    return a


def heights_sum(n: int) -> int:
    """Formal proof of Section 8.4: the heights of all n positions of a heap add up to fewer than n."""
    total = 0
    for i in range(n):
        h = 0
        while 2 ** (h + 1) * (i + 1) <= n:
            h += 1
        total += h
    return total


if __name__ == "__main__":
    print(sort_nearly_sorted([25, 12, 47, 31, 58, 70, 63, 91, 84], 1))
    print(heapsort_top_down_build([12, 25, 31, 47]))
    print([heights_sum(n) for n in range(1, 17)])
