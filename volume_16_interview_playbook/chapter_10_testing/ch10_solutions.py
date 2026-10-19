"""Volume 16, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations


def binary_search_fixed(nums: list[int], target: int) -> int:
    """Exercise 1: the classic bug is writing `while lo <= hi` together with `hi = mid`, which loops forever once
    lo == hi. The fix: loop while lo < hi, then check the one remaining candidate."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if nums and nums[lo] == target else -1


def edge_cases_for_string() -> list[str]:
    """Exercise 2: the standard checklist for string inputs."""
    return ["", "a", "aa", "ab", "aba", "abc" * 3, " ", "Aa", "z" * 50]


def edge_cases_for_grid() -> list[list[str]]:
    """Exercise 3: the standard checklist for grid inputs."""
    return [["1"], ["0"], ["111"], ["1", "1", "1"], ["10", "01"], ["11", "11"], ["000", "000"]]


if __name__ == "__main__":
    print(binary_search_fixed([1, 3, 5, 7], 5), binary_search_fixed([], 1), len(edge_cases_for_string()), len(edge_cases_for_grid()))
