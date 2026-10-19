"""Volume 16, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """Exercise 1 (LeetCode 560): count subarrays summing to k - prefix sums plus a hash map of seen prefixes."""
    seen = Counter({0: 1})
    total = running = 0
    for x in nums:
        running += x
        total += seen[running - k]
        seen[running] += 1
    return total


def character_replacement(s: str, k: int) -> int:
    """Exercise 2 (LeetCode 424): longest substring that becomes one repeated letter after at most k changes."""
    counts: Counter[str] = Counter()
    left = best = top = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        top = max(top, counts[ch])
        while right - left + 1 - top > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def is_valid_sudoku_rows(board: list[list[str]]) -> bool:
    """Exercise 3 (LeetCode 36): no digit repeats in a row, column or 3x3 box - one set of seen keys."""
    seen = set()
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == ".":
                continue
            keys = {("row", r, d), ("col", c, d), ("box", r // 3, c // 3, d)}
            if keys & seen:
                return False
            seen |= keys
    return True


if __name__ == "__main__":
    print(subarray_sum_equals_k([1, 1, 1], 2), character_replacement("AABABBA", 1))
