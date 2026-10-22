"""Volume 1, Chapter 20 - Binary Search on Answers.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

import math

BOXES = [5, 9, 3, 7, 4, 8, 2, 6]      # kilograms, in the order they must travel


def trips_needed(boxes: list[int], capacity: int) -> int:
    """Greedy loading in order: start a new trip whenever the next box would not fit (Figure 20.2)."""
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
    """Smallest x in [lo, hi] with ok(x) True, given ok is False ... False True ... True (Figure 20.3)."""
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


def last_true(lo: int, hi: int, ok, trace: list | None = None) -> int:
    """Largest x in [lo, hi] with ok(x) True, given ok is True ... True False ... False and ok(lo) is True.
    The middle is rounded UP, so lo <- mid always moves lo (Section 20.6)."""
    while lo < hi:
        mid = (lo + hi + 1) // 2
        good = ok(mid)
        if trace is not None:
            trace.append((lo, hi, mid, good))
        if good:
            lo = mid
        else:
            hi = mid - 1
    return lo


def last_true_rounding_down(lo: int, hi: int, ok, max_rounds: int = 20) -> tuple[int, int, int]:
    """The buggy version with mid = (lo + hi) // 2, stopped after max_rounds rounds; returns (lo, hi, rounds).
    Once hi = lo + 1 the middle is lo itself, a "yes" sets lo <- lo, and the range never shrinks again."""
    rounds = 0
    while lo < hi and rounds < max_rounds:
        rounds += 1
        mid = (lo + hi) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo, hi, rounds


def pieces(ropes: list[int], length: int) -> int:
    """How many pieces of the given whole-metre length the ropes give (leftovers thrown away)."""
    return sum(r // length for r in ropes)


def longest_piece(ropes: list[int], k: int, trace: list | None = None) -> int:
    """Longest whole length giving at least k pieces; 0 if not even length 1 works (Challenge 20.1)."""
    if pieces(ropes, 1) < k:
        return 0
    return last_true(1, max(ropes), lambda L: pieces(ropes, L) >= k, trace)


def lamps_fit(desks: list[int], k: int, gap: int) -> bool:
    """Can k lamps go on desks (sorted positions in metres) with every two lamps at least gap apart? Greedy from the left."""
    placed, last = 0, None
    for d in desks:
        if last is None or d - last >= gap:
            placed, last = placed + 1, d
    return placed >= k


def widest_spacing(desks: list[int], k: int) -> int:
    """Largest smallest gap between k lamps on the sorted desks (Challenge 20.1); needs 2 <= k <= len(desks)."""
    return last_true(1, desks[-1] - desks[0], lambda g: lamps_fit(desks, k, g))


def real_threshold(lo: float, hi: float, ok, rounds: int) -> float:
    """Search on real numbers: ok is False ... True on [lo, hi]; halve the interval a fixed number of times
    and return the right end, which always passes (Section 20.6)."""
    for _ in range(rounds):
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


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
