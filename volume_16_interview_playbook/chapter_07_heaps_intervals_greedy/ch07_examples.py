"""Volume 16, Chapter 7 - Heaps, Intervals, and Greedy: Interview Drill.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import heapq
from collections import Counter


def kth_largest(nums: list[int], k: int) -> int:
    """LeetCode 215: keep a min-heap of the k largest seen so far; its top is the answer. O(n log k)."""
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """LeetCode 347: count, then bucket by frequency - O(n), no sorting of all counts."""
    counts = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for value, c in counts.items():
        buckets[c].append(value)
    out: list[int] = []
    for c in range(len(nums), 0, -1):
        for value in sorted(buckets[c]):
            out.append(value)
            if len(out) == k:
                return out
    return out


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """LeetCode 56: sort by start; extend the last merged interval while the next one overlaps."""
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """LeetCode 57: copy the intervals before, absorb the overlapping ones, copy the intervals after. O(n)."""
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:
        out.append(intervals[i])
        i += 1
    start, end = new
    while i < n and intervals[i][0] <= end:
        start, end = min(start, intervals[i][0]), max(end, intervals[i][1])
        i += 1
    return out + [[start, end]] + intervals[i:]


def min_removals(intervals: list[list[int]]) -> int:
    """LeetCode 435: fewest removals so the rest don't overlap = n - most non-overlapping (earliest end first, V10-C4)."""
    kept, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:
            kept += 1
            last_end = end
    return len(intervals) - kept


def meeting_rooms(intervals: list[list[int]]) -> int:
    """LeetCode 253: a min-heap of end times of meetings in progress; its size peaks at the rooms needed."""
    ends: list[int] = []
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)


def can_jump(nums: list[int]) -> bool:
    """LeetCode 55: greedy - track the farthest index reachable so far."""
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True


def busiest_hour(bookings: list[list[int]]) -> int:
    """Industry example: the most rooms ever booked at once in a meeting system."""
    return meeting_rooms(bookings)


if __name__ == "__main__":
    print(kth_largest([3, 2, 1, 5, 6, 4], 2), top_k_frequent([1, 1, 1, 2, 2, 3], 2))
    print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]), insert_interval([[1, 3], [6, 9]], [2, 5]))
    print(min_removals([[1, 2], [2, 3], [3, 4], [1, 3]]), meeting_rooms([[0, 30], [5, 10], [15, 20]]))
    print(can_jump([2, 3, 1, 1, 4]), can_jump([3, 2, 1, 0, 4]), busiest_hour([[9, 10], [9, 12], [11, 13], [12, 14]]))
