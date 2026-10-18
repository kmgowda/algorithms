"""Volume 4, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations


def has_duplicate_three_ways(values: list[int]) -> tuple[bool, bool, bool]:
    """Exercise 1 (LeetCode 217): brute force, sorting, hashing - all must agree."""
    brute = any(values[i] == values[j] for i in range(len(values)) for j in range(i + 1, len(values)))
    s = sorted(values)
    by_sort = any(s[i] == s[i + 1] for i in range(len(s) - 1))
    by_hash = len(set(values)) != len(values)
    return brute, by_sort, by_hash


def longest_stretch_sum_at_most(values: list[int], limit: int) -> int:
    """Exercise 2: longest consecutive stretch with sum <= limit, values non-negative -> sliding window."""
    left = total = best = 0
    for right, v in enumerate(values):
        total += v
        while total > limit:
            total -= values[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def longest_stretch_sum_exactly(values: list[int], target: int) -> int:
    """Exercise 3: longest stretch with sum exactly target, negatives allowed -> prefix sums + first-seen index."""
    first = {0: -1}
    running = best = 0
    for i, v in enumerate(values):
        running += v
        if running - target in first:
            best = max(best, i - first[running - target])
        first.setdefault(running, i)
    return best


if __name__ == "__main__":
    print(has_duplicate_three_ways([3, 1, 4, 1]), longest_stretch_sum_at_most([2, 1, 3, 4, 1], 6),
          longest_stretch_sum_exactly([1, -1, 5, -2, 3], 3))
