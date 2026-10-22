"""Volume 4, Chapter 4 - Thinking Problems (Section 4.15): model solutions.

Run:  python3 ch04_solutions.py
"""

from __future__ import annotations

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def count_close_pairs(days: list, d: int) -> int:
    """Thinking Problem 2: pairs whose values differ by at most d, by sorting then two pointers."""
    s = sorted(days)
    count = left = 0
    for right in range(len(s)):
        while s[right] - s[left] > d:
            left += 1
        count += right - left
    return count


def total_displacement(a: list) -> int:
    """Thinking Problem 3: the sum over items of |position now - position when sorted| (ties kept in order)."""
    order = sorted(range(len(a)), key=lambda i: a[i])
    return sum(abs(i - r) for r, i in enumerate(order))


if __name__ == "__main__":
    print(count_close_pairs(PILE, 10), total_displacement(PILE))
