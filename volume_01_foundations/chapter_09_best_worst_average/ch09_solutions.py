"""Volume 1, Chapter 9, Thinking Problem 2 - a whole day's requests in one pass.

Run:  python3 ch09_solutions.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def day_summary(shelf: list[int], requests: list[int]) -> tuple[int, int, float]:
    """Best, worst and average looks linear search needs over a log of requests, in O(n + m) time:
    a dictionary remembers each book's position (the first copy, as linear search finds it), and a
    missing book costs len(shelf) looks. No requests gives (0, 0, 0.0)."""
    where: dict[int, int] = {}
    for p, book in enumerate(shelf, start=1):
        if book not in where:
            where[book] = p
    if not requests:
        return 0, 0, 0.0
    best, worst, total = len(shelf), 0, 0
    for target in requests:
        cost = where.get(target, len(shelf))
        best, worst, total = min(best, cost), max(worst, cost), total + cost
    return best, worst, total / len(requests)


if __name__ == "__main__":
    print(day_summary(SHELF, [12, 91, 50, 63]))
