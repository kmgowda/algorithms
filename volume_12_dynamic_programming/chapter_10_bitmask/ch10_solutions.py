"""Volume 12, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache


def count_subsets_with_sum(values: list[int], target: int) -> int:
    """Exercise 1: loop over every mask (2^n subsets) and add the chosen values - the simplest bitmask brute force."""
    n = len(values)
    return sum(1 for mask in range(1 << n) if sum(values[i] for i in range(n) if mask >> i & 1) == target)


def can_partition_k_bitmask(values: list[int], k: int) -> bool:
    """Exercise 2 (LeetCode 698): k equal-sum groups. State = mask of used values; the running total
    modulo the group size tells how full the current group is."""
    total = sum(values)
    if total % k:
        return False
    goal, n = total // k, len(values)

    @lru_cache(maxsize=None)
    def ok(mask: int, filled: int) -> bool:
        if mask == (1 << n) - 1:
            return True
        for i in range(n):
            if not mask >> i & 1 and filled + values[i] <= goal:
                if ok(mask | 1 << i, (filled + values[i]) % goal):
                    return True
        return False

    return ok(0, 0)


def count_beautiful_arrangements(n: int) -> int:
    """Exercise 3 (LeetCode 526): orderings of 1..n where position p (1-based) and number x satisfy
    p % x == 0 or x % p == 0. State = mask of numbers already placed."""
    @lru_cache(maxsize=None)
    def ways(mask: int) -> int:
        p = bin(mask).count("1") + 1
        if p > n:
            return 1
        return sum(ways(mask | 1 << (x - 1)) for x in range(1, n + 1)
                   if not mask >> (x - 1) & 1 and (p % x == 0 or x % p == 0))
    return ways(0)


if __name__ == "__main__":
    print(count_subsets_with_sum([1, 2, 3, 4, 5], 5), can_partition_k_bitmask([4, 3, 2, 3, 5, 2, 1], 4),
          count_beautiful_arrangements(4))
