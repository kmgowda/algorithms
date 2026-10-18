"""Volume 5, Chapter 2 - Binary Search Variants: Bounds, Rotated Arrays, Peaks.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from typing import Sequence


def lower_bound(items: Sequence, target) -> int:
    """First index whose item is >= target (len(items) if none). Same as bisect.bisect_left."""
    low, high = 0, len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def upper_bound(items: Sequence, target) -> int:
    """First index whose item is > target. Same as bisect.bisect_right."""
    low, high = 0, len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low


def find_range(items: Sequence, target) -> tuple[int, int]:
    """LeetCode 34: first and last positions of target, (-1, -1) if absent."""
    first = lower_bound(items, target)
    if first == len(items) or items[first] != target:
        return -1, -1
    return first, upper_bound(items, target) - 1


def count_between(items: Sequence, low_value, high_value) -> int:
    """How many items fall in [low_value, high_value]? Two bounds, no scanning."""
    return upper_bound(items, high_value) - lower_bound(items, low_value)


def search_rotated(items: list[int], target: int) -> int:
    """LeetCode 33: a sorted list rotated at an unknown point (e.g. a circular timetable). O(log n).

    At every step, one half is still sorted; check whether the target lies inside that half.
    """
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        if items[low] <= items[mid]:                      # left half sorted
            if items[low] <= target < items[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:                                             # right half sorted
            if items[mid] < target <= items[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1


def rotation_point(items: list[int]) -> int:
    """LeetCode 153: index of the smallest item in a rotated sorted list (distinct values)."""
    low, high = 0, len(items) - 1
    while low < high:
        mid = (low + high) // 2
        if items[mid] > items[high]:
            low = mid + 1
        else:
            high = mid
    return low


def find_peak(heights: list[int]) -> int:
    """LeetCode 162: an index higher than its neighbours (edges count as -infinity). Walk uphill by halves."""
    low, high = 0, len(heights) - 1
    while low < high:
        mid = (low + high) // 2
        if heights[mid] < heights[mid + 1]:
            low = mid + 1
        else:
            high = mid
    return low


def shipping_rate(weight_kg: float, limits: list[float], rates: list[float]) -> float:
    """Industry example: price tiers. limits are tier upper bounds (sorted); rates has one extra 'above all' rate."""
    return rates[lower_bound(limits, weight_kg)]


def logs_between(timestamps: list[int], start: int, end: int) -> tuple[int, int]:
    """Industry example: sorted log timestamps - which slice covers [start, end]? Returns (first, last+1)."""
    return lower_bound(timestamps, start), upper_bound(timestamps, end)


if __name__ == "__main__":
    scores = [55, 60, 60, 60, 72, 88, 88, 95]
    print(lower_bound(scores, 60), upper_bound(scores, 60), find_range(scores, 88), count_between(scores, 60, 88))
    timetable = [14, 16, 19, 22, 6, 8, 11]
    print(search_rotated(timetable, 8), rotation_point(timetable), find_peak([1, 3, 7, 4, 2, 5, 1]))
    print(shipping_rate(3.2, [1, 5, 10], [50, 120, 200, 400]))
    print(logs_between([100, 105, 110, 110, 130, 150], 105, 130))
