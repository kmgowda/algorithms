"""Volume 10, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def min_arrows(balloons: list[tuple[int, int]]) -> int:
    """Exercise 1 (LeetCode 452): fewest arrows to burst all balloons (intervals). Shoot at the earliest end."""
    arrows, last = 0, float("-inf")
    for start, end in sorted(balloons, key=lambda b: b[1]):
        if start > last:
            arrows += 1
            last = end
    return arrows


def erase_overlaps(intervals: list[tuple[int, int]]) -> int:
    """Exercise 2 (LeetCode 435): fewest intervals to remove so the rest don't overlap = total - max kept."""
    kept, last = 0, float("-inf")
    for s, e in sorted(intervals, key=lambda iv: iv[1]):
        if s >= last:
            kept += 1
            last = e
    return len(intervals) - kept


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Exercise 3 (LeetCode 56): merge overlapping bookings - sort by start, extend the current block."""
    out: list[list[int]] = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]                 # type: ignore[misc]


def min_platforms(arrivals: list[int], departures: list[int]) -> int:
    """Exercise 4 (industry): train platforms needed - sweep arrivals and departures in time order."""
    events = sorted([(a, 1) for a in arrivals] + [(d, -1) for d in departures], key=lambda x: (x[0], -x[1]))
    current = best = 0
    for _, change in events:
        current += change
        best = max(best, current)
    return best


if __name__ == "__main__":
    print(min_arrows([(10, 16), (2, 8), (1, 6), (7, 12)]), erase_overlaps([(1, 2), (2, 3), (3, 4), (1, 3)]),
          merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]), min_platforms([900, 940, 950, 1100], [910, 1200, 1120, 1130]))
