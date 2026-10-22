"""Volume 7, Chapter 16 - Thinking Problem 2: how many pairs of bookings overlap? O(n log n), however many there are.

Run:  python3 ch16_solutions.py
"""

from __future__ import annotations

from ch16_examples import BOOKINGS


def overlapping_pairs(intervals: list) -> int:
    """Count pairs of half-open intervals [s, e) that share a moment. Sweep with a counter of open intervals
    (ends before starts at equal times); each new start overlaps exactly the intervals open at that moment."""
    events = sorted([(s, 1) for s, _ in intervals] + [(e, -1) for _, e in intervals])
    open_now = pairs = 0
    for _, d in events:
        if d == 1:
            pairs += open_now
        open_now += d
    return pairs


if __name__ == "__main__":
    print(overlapping_pairs(BOOKINGS))
