"""Volume 1, Chapter 10, Thinking Problem 2 - squeezing out repeated returns in place.

Run:  python3 ch10_solutions.py
"""

from __future__ import annotations

SORTED_RETURNS = [12, 12, 25, 31, 31, 31, 47, 63, 63]


def compact_sorted(shelf: list[int]) -> int:
    """Move one copy of each value of a sorted list to its front, in order, and return how many there are.
    Two pointers (read, write): O(n) time and O(1) extra space; the items after the answer are left over."""
    if not shelf:
        return 0
    write = 1
    for read in range(1, len(shelf)):
        if shelf[read] != shelf[write - 1]:
            shelf[write] = shelf[read]
            write += 1
    return write


if __name__ == "__main__":
    s = SORTED_RETURNS[:]
    k = compact_sorted(s)
    print(k, s[:k])
