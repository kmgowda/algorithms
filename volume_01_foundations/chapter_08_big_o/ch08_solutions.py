"""Volume 1, Chapter 8, Thinking Problem 2 - the busiest stretch of k consecutive days in O(n) steps.

Run:  python3 ch08_solutions.py
"""

from __future__ import annotations


def busiest_stretch(visits: list[int], k: int) -> tuple[int, int]:
    """First start position and visitor total of the busiest run of k consecutive days (1 <= k <= len(visits)).

    The window total is kept up to date as the window slides one day to the right: add the day that enters,
    subtract the day that leaves. That is O(n) work instead of O(n * k) for adding up every window afresh."""
    total = 0
    for d in range(k):
        total = total + visits[d]
    best, start = total, 0
    for i in range(1, len(visits) - k + 1):
        total = total + visits[i + k - 1] - visits[i - 1]
        if total > best:
            best, start = total, i
    return start, best


if __name__ == "__main__":
    week = [34, 41, 29, 56, 48, 61, 22]
    print(busiest_stretch(week, 3), busiest_stretch(week, 1), busiest_stretch(week, 7))
