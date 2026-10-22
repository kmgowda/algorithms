"""Volume 1, Chapter 13, Thinking Problem 2 - the largest item by splitting in half.

`largest` (ch13_examples) peels off one item per call, so a list of 2,000 items needs 2,000 nested calls and
Python stops it with RecursionError. Splitting the range in half keeps the recursion only about log2 n deep
and still makes exactly n - 1 comparisons.

Run:  python3 ch13_solutions.py
"""

from __future__ import annotations


def largest_split(items: list[int], low: int, high: int) -> int:
    """The largest of items[low..high] (low <= high): the larger of the largest in each half."""
    if low == high:
        return items[low]
    mid = (low + high) // 2
    left = largest_split(items, low, mid)
    right = largest_split(items, mid + 1, high)
    return left if left >= right else right


def largest_split_costs(size: int) -> tuple[int, int]:
    """(comparisons, deepest frames) made by largest_split on a range of `size` >= 1 items."""
    if size == 1:
        return 0, 1
    left, right = largest_split_costs((size + 1) // 2), largest_split_costs(size // 2)
    return left[0] + right[0] + 1, 1 + max(left[1], right[1])


def largest_of(items: list[int]) -> int:
    """The largest item of a non-empty list; an empty list has no largest item (ValueError)."""
    if not items:
        raise ValueError("an empty list has no largest item")
    return largest_split(items, 0, len(items) - 1)


if __name__ == "__main__":
    shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
    print(largest_of(shelf), largest_split_costs(len(shelf)), largest_split_costs(2000))
    print(largest_of(list(range(5000))))
