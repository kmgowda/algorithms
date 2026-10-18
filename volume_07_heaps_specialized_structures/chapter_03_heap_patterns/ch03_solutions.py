"""Volume 7, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

import heapq
from collections import Counter


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """Exercise 1 (LeetCode 347/692): k most frequent words, ties alphabetical."""
    counts = Counter(words)
    return heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w))


def kth_smallest_in_sorted_rows(grid: list[list[int]], k: int) -> int:
    """Exercise 2 (LeetCode 378): rows sorted; k-way merge, stop after k pops."""
    heap = [(row[0], r, 0) for r, row in enumerate(grid) if row]
    heapq.heapify(heap)
    value = 0
    for _ in range(k):
        value, r, c = heapq.heappop(heap)
        if c + 1 < len(grid[r]):
            heapq.heappush(heap, (grid[r][c + 1], r, c + 1))
    return value


def min_meeting_rooms(meetings: list[tuple[int, int]]) -> int:
    """Exercise 3 (LeetCode 253): a min-heap of end times of meetings in progress."""
    ends: list[int] = []
    for start, end in sorted(meetings):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)


def sliding_median(values: list[float], k: int) -> list[float]:
    """Exercise 4 (LeetCode 480, simple version): median of each window of k, by sorting each window. O(n k log k)."""
    out = []
    for i in range(len(values) - k + 1):
        w = sorted(values[i:i + k])
        out.append(w[k // 2] if k % 2 else (w[k // 2 - 1] + w[k // 2]) / 2)
    return out


if __name__ == "__main__":
    print(top_k_frequent("the lion and the zebra and the bird".split(), 2))
    print(kth_smallest_in_sorted_rows([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8))
    print(min_meeting_rooms([(9, 10), (9, 12), (11, 13), (13, 14)]), sliding_median([1, 3, -1, -3, 5, 3], 3))
