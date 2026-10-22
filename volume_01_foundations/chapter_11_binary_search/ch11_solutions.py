"""Volume 1, Chapter 11, Thinking Problem 2 - the slot that matches its label.

Run:  python3 ch11_solutions.py
"""

from __future__ import annotations

CASE = [-4, -1, 1, 3, 6, 9, 11]


def matching_slot(a: list[int]) -> int:
    """First position i with a[i] == i in a sorted list of DISTINCT whole numbers, or -1 if there is none.
    a[i] - i never decreases, so a lower-bound search on "a[i] >= i" finds it in O(log n) looks."""
    low, high = 0, len(a)
    while low < high:
        mid = (low + high) // 2
        if a[mid] < mid:
            low = mid + 1
        else:
            high = mid
    if low < len(a) and a[low] == low:
        return low
    return -1


if __name__ == "__main__":
    print(matching_slot(CASE), matching_slot([1, 1, 1]))
