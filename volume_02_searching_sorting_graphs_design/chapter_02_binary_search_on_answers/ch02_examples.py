"""Volume 2, Chapter 2 - Binary Search on Answers.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import math

BOXES = [5, 9, 3, 7, 4, 8, 2, 6]      # kilograms, in the order they must travel


def trips_needed(boxes: list[int], capacity: int) -> int:
    """Greedy loading in order: start a new trip whenever the next box would not fit (Figure 2.2)."""
    trips, load = 1, 0
    for b in boxes:
        if load + b > capacity:
            trips, load = trips + 1, 0
        load += b
    return trips


def loads(boxes: list[int], capacity: int) -> list[list[int]]:
    out, cur = [[]], 0
    for b in boxes:
        if cur + b > capacity:
            out.append([])
            cur = 0
        out[-1].append(b)
        cur += b
    return out


def first_true(lo: int, hi: int, ok, trace: list | None = None) -> int:
    """Smallest x in [lo, hi] with ok(x) True, given ok is False ... False True ... True (Figure 2.3)."""
    while lo < hi:
        mid = (lo + hi) // 2
        good = ok(mid)
        if trace is not None:
            trace.append((lo, hi, mid, good))
        if good:
            hi = mid
        else:
            lo = mid + 1
    return lo


def smallest_capacity(boxes: list[int], max_trips: int, trace: list | None = None) -> int:
    """The answer lies between the heaviest box and the total weight."""
    return first_true(max(boxes), sum(boxes), lambda c: trips_needed(boxes, c) <= max_trips, trace)


def slowest_reading_speed(books: list[int], hours: int) -> int:
    """Smallest pages-per-hour so every book (one at a time, whole hours per book) is read within the hours."""
    return first_true(1, max(books), lambda s: sum(math.ceil(p / s) for p in books) <= hours)


def brute_capacity(boxes: list[int], max_trips: int) -> int:
    c = max(boxes)
    while trips_needed(boxes, c) > max_trips:
        c += 1
    return c


if __name__ == "__main__":
    for c in range(9, 45):
        print(c, trips_needed(BOXES, c), end="; ")
    print()
    t = []
    print(smallest_capacity(BOXES, 3, t), t, loads(BOXES, 16))
    print(slowest_reading_speed([300, 120, 450, 210], 8))
    print(smallest_capacity(BOXES, 2), smallest_capacity(BOXES, 4))
