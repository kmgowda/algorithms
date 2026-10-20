"""Volume 1, Chapter 1 - What Is an Algorithm?

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]
HEIGHTS = [142, 155, 138, 161, 150, 158]


def tallest(heights: list[int]) -> int:
    """Return the largest height in a non-empty list, looking at each height once."""
    tallest_so_far = heights[0]
    for h in heights[1:]:
        if h > tallest_so_far:
            tallest_so_far = h
    return tallest_so_far


def looks_one_by_one(shelf: list[int], wanted: int) -> int:
    """Way A (Figure 1.7): how many books are looked at, from the left, until `wanted` is found."""
    for looks, call_number in enumerate(shelf, start=1):
        if call_number == wanted:
            return looks
    return len(shelf)


def looks_by_halving(shelf: list[int], wanted: int) -> int:
    """Way B (Figure 1.7): how many books are looked at when each look discards half of a sorted shelf."""
    low, high, looks = 0, len(shelf) - 1, 0
    while low <= high:
        middle = (low + high) // 2
        looks += 1
        if shelf[middle] == wanted:
            return looks
        if shelf[middle] < wanted:
            low = middle + 1
        else:
            high = middle - 1
    return looks


if __name__ == "__main__":
    print("tallest:", tallest(HEIGHTS))
    print("book 63:", looks_one_by_one(SHELF, 63), "looks one by one,", looks_by_halving(SHELF, 63), "by halving")
    print("book 91:", looks_one_by_one(SHELF, 91), "looks one by one,", looks_by_halving(SHELF, 91), "by halving")
