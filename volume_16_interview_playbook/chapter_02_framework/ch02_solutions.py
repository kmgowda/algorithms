"""Volume 16, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations


def two_sum_sorted(nums: list[int], target: int) -> list[int] | None:
    """Exercise 1 (LeetCode 167): the input is SORTED - two pointers give O(1) memory (V4-C5)."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None


def count_pairs(nums: list[int], target: int) -> int:
    """Exercise 2: how many index pairs i < j sum to target - count earlier complements in a dictionary."""
    seen: dict[int, int] = {}
    total = 0
    for x in nums:
        total += seen.get(target - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return total


def contains_duplicate(nums: list[int]) -> bool:
    """Exercise 3 (LeetCode 217): apply the framework - brute force pairs O(n^2), improve with a set O(n)."""
    return len(set(nums)) != len(nums)


if __name__ == "__main__":
    print(two_sum_sorted([2, 7, 11, 15], 9), count_pairs([1, 5, 7, -1, 5], 6), contains_duplicate([1, 2, 3, 1]))
