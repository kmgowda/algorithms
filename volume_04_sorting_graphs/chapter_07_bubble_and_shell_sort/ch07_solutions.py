"""Volume 4, Chapter 7 - Thinking Problems (Section 7.15): model solutions.

Run:  python3 ch07_solutions.py
"""

from __future__ import annotations

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def larger_before(a: list) -> list[int]:
    """Thinking Problem 1: for each item, how many larger items stand before it (O(n^2), for checking)."""
    return [sum(1 for k in range(i) if a[k] > a[i]) for i in range(len(a))]


def predict_bubble_passes(a: list) -> tuple[int, int]:
    """Thinking Problem 2: the passes and comparisons bubble sort with early exit will make, in O(n log n)."""
    n = len(a)
    if n < 2:
        return 0, 0
    order = sorted(range(n), key=lambda i: a[i])          # stable: equal items keep their order
    p = [0] * n
    for r, i in enumerate(order):
        p[i] = r
    passes = min(n - 1, max(i - p[i] for i in range(n)) + 1)
    return passes, passes * (n - 1) - passes * (passes - 1) // 2


def is_h_sorted(a: list, h: int) -> bool:
    """Thinking Problem 3: every item is no larger than the item h places after it."""
    return all(a[i] <= a[i + h] for i in range(len(a) - h))


if __name__ == "__main__":
    print(larger_before(PILE), predict_bubble_passes(PILE))
    print(is_h_sorted([2, 1, 4, 3], 2), is_h_sorted([2, 1, 4, 3], 3))
