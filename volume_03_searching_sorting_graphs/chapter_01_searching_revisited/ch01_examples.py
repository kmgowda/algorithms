"""Volume 3, Chapter 1 - Searching Revisited: lower bound, upper bound, counting, and ranges.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import bisect

CATALOGUE = [12, 25, 25, 31, 47, 47, 47, 58, 63, 70, 84, 91]


def lower_bound(a: list, key, trace: list | None = None) -> int:
    """First position whose value is >= key. Invariant: a[:lo] < key <= a[hi:] (Figure 1.2)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if trace is not None:
            trace.append((lo, hi, mid, a[mid]))
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a: list, key) -> int:
    """First position whose value is > key."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= key:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count(a: list, key) -> int:
    return upper_bound(a, key) - lower_bound(a, key)


def count_between(a: list, low, high) -> int:
    """How many values lie in [low, high]: two searches, O(log n)."""
    return upper_bound(a, high) - lower_bound(a, low)


def contains(a: list, key) -> bool:
    i = lower_bound(a, key)
    return i < len(a) and a[i] == key


def due_date_report(due: list[int], today: int, week_end: int, new_day: int) -> tuple[int, int, int]:
    """Section 1.7: (due today, due this week, insertion position for a new loan)."""
    return (count(due, today), count_between(due, today, week_end), upper_bound(due, new_day))


if __name__ == "__main__":
    t = []
    print(lower_bound(CATALOGUE, 47, t), t)
    print(upper_bound(CATALOGUE, 47), count(CATALOGUE, 47), count_between(CATALOGUE, 30, 65))
    t = []
    print(lower_bound(CATALOGUE, 50, t), t, contains(CATALOGUE, 50))
    print(bisect.bisect_left(CATALOGUE, 47), bisect.bisect_right(CATALOGUE, 47))
