"""Volume 5, Chapter 1 - Searching Revisited: Linear, Binary, and Binary Search on the Answer.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from typing import Callable, Sequence


def linear_search(items: Sequence, target) -> int:
    """Works on anything, sorted or not. O(n)."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


def binary_search(sorted_items: Sequence, target) -> int:
    """Halve the search range each step. Needs sorted input. O(log n)."""
    low, high = 0, len(sorted_items) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        if sorted_items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def first_true(low: int, high: int, ok: Callable[[int], bool]) -> int:
    """The general tool: ok(x) is False...False, True...True over low..high. Return the first True (high+1 if none).

    This 'monotone yes/no question' view is what makes binary search on the answer possible.
    """
    while low <= high:
        mid = (low + high) // 2
        if ok(mid):
            high = mid - 1
        else:
            low = mid + 1
    return low


def integer_sqrt(n: int) -> int:
    """LeetCode 69: the largest r with r*r <= n, by asking 'is (r+1)^2 > n?'."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return first_true(0, n, lambda r: (r + 1) * (r + 1) > n)


def monkey_eating_speed(bananas: list[int], hours: int) -> int:
    """LeetCode 875: a zoo monkey eats at most `speed` bananas per hour, one pile at a time.
    What's the slowest speed that finishes all piles within `hours`?"""
    def finishes(speed: int) -> bool:
        return sum((pile + speed - 1) // speed for pile in bananas) <= hours
    return first_true(1, max(bananas), finishes)


def split_shelves(book_widths: list[int], shelves: int) -> int:
    """LeetCode 410 idea: split books (in order) onto `shelves` shelves so the widest shelf is as narrow as possible."""
    def fits(width: int) -> bool:
        used, current = 1, 0
        for w in book_widths:
            if current + w > width:
                used, current = used + 1, 0
            current += w
        return used <= shelves
    return first_true(max(book_widths), sum(book_widths), fits)


def first_bad_version(versions: int, is_bad: Callable[[int], bool]) -> int:
    """Industry example (like 'git bisect'): versions 1..n, good then bad. Find the first bad one in O(log n) tests."""
    return first_true(1, versions, is_bad)


if __name__ == "__main__":
    shelf = ["Atlas", "Birds", "Cats", "Dune", "Emma", "Fables"]
    print(linear_search(["zebra", "lion", "otter"], "otter"), binary_search(shelf, "Dune"))
    print("sqrt(80) =", integer_sqrt(80), "| monkey speed:", monkey_eating_speed([3, 6, 7, 11], 8))
    print("narrowest widest shelf:", split_shelves([7, 2, 5, 10, 8], 2))
    print("first bad build:", first_bad_version(100, lambda v: v >= 64))
