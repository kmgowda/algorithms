"""Volume 1, Chapter 12, Thinking Problem 2 - Maya's staircase display.

Run:  python3 ch12_solutions.py
"""

from __future__ import annotations


def staircase_steps(books: int) -> int:
    """The most complete steps (1 book, then 2, then 3, ...) that `books` books can build: the largest k with
    k(k + 1)/2 <= books. Binary search on the answer with a rounded-up midpoint: O(log n) rounds."""
    low, high = 0, books
    while low < high:
        mid = (low + high + 1) // 2
        if mid * (mid + 1) // 2 <= books:
            low = mid
        else:
            high = mid - 1
    return low


if __name__ == "__main__":
    print([staircase_steps(n) for n in (0, 1, 2, 3, 100)])
