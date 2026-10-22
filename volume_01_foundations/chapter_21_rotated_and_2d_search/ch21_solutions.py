"""Volume 1, Chapter 21, Thinking Problem 2 - counting a range of call numbers on the turned shelf.

The shelf is a rotated sorted list of distinct values. Find the rotation point, then count the values in
[low, high] in each of the two sorted runs with a lower and an upper bound: O(log n) looks in all.

Run:  python3 ch21_solutions.py
"""

from __future__ import annotations

import bisect

from ch21_examples import ROTATED, find_rotation


def count_in_range_rotated(a: list, low, high) -> int:
    """How many values v of the rotated sorted list a have low <= v <= high (distinct values)."""
    if not a or low > high:
        return 0
    s = find_rotation(a)
    count = 0
    for first, last in ((s, len(a)), (0, s)):          # the two sorted runs, as half-open ranges
        count += bisect.bisect_right(a, high, first, last) - bisect.bisect_left(a, low, first, last)
    return count


if __name__ == "__main__":
    print(count_in_range_rotated(ROTATED, 30, 70))      # 31, 47, 58, 63, 70 -> 5
