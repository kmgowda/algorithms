"""Volume 1, Chapter 10 - Space Complexity.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]
RETURNS = [47, 12, 63, 25, 63, 91, 31, 70, 84]


def reverse_in_place(shelf: list[int]) -> None:
    """Reverse the list using two pointers that swap and move inward: O(n) time, O(1) extra space."""
    left, right = 0, len(shelf) - 1
    while left < right:
        shelf[left], shelf[right] = shelf[right], shelf[left]
        left, right = left + 1, right - 1


def reverse_by_copying(shelf: list[int]) -> list[int]:
    """Build a reversed copy: O(n) time and O(n) extra space (Figure 10.2)."""
    return [shelf[i] for i in range(len(shelf) - 1, -1, -1)]


def has_duplicate_pairs(items: list[int]) -> tuple[bool, int]:
    """Compare every pair (no extra memory). Returns (answer, comparisons made)."""
    comparisons = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            comparisons += 1
            if items[i] == items[j]:
                return True, comparisons
    return False, comparisons


def first_duplicate_with_memory(items: list[int]) -> tuple[int | None, int]:
    """Remember what has been seen (O(n) extra space). Returns (first repeated item, items checked)."""
    seen = set()
    for k, item in enumerate(items, start=1):
        if item in seen:
            return item, k
        seen.add(item)
    return None, len(items)


if __name__ == "__main__":
    s = SHELF[:]
    reverse_in_place(s)
    print(s, reverse_by_copying(SHELF))
    print(has_duplicate_pairs(list(range(9))), first_duplicate_with_memory(RETURNS))
