"""Volume 1, Chapter 11 - Binary Search.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def binary_search(shelf: list[int], target: int) -> tuple[int, int, list[int]]:
    """Plain binary search (Figures 11.1 and 11.2). Returns (position or -1, final low, positions looked at)."""
    low, high, looked = 0, len(shelf) - 1, []
    while low <= high:
        mid = (low + high) // 2
        looked.append(mid)
        if shelf[mid] == target:
            return mid, low, looked
        if shelf[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, low, looked


def lower_bound(shelf: list[int], target: int) -> int:
    """First position whose item is >= target (len(shelf) if none): the insertion point (Figure 11.5)."""
    low, high = 0, len(shelf)
    while low < high:
        mid = (low + high) // 2
        if shelf[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def worst_looks(n: int) -> int:
    """floor(log2 n) + 1: the most looks binary search needs on n items (Figure 11.4)."""
    return n.bit_length()


if __name__ == "__main__":
    print(binary_search(SHELF, 63), binary_search(SHELF, 50), binary_search(SHELF, 25))
    print(lower_bound([12, 25, 47, 47, 47, 63, 70, 84, 91], 47), binary_search(SHELF, 95)[1])
    print([worst_looks(n) for n in (9, 100, 1000, 4000, 10 ** 6, 10 ** 9)])
    print(binary_search([47, 12, 91, 25], 25))
