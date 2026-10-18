"""Volume 12, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache


def brute_trades(prices: list[int], k: int | None = None, cooldown: int = 0, fee: int = 0) -> int:
    """Exercise 1: an obviously correct reference - try buy/sell/wait on every day (memoized on the state)."""
    limit = len(prices) if k is None else k

    @lru_cache(maxsize=None)
    def go(day: int, holding: bool, trades: int) -> int:
        if day >= len(prices):
            return 0
        best = go(day + 1, holding, trades)                       # wait
        if holding:
            best = max(best, prices[day] - fee + go(day + 1 + cooldown, False, trades))
        elif trades < limit:
            best = max(best, -prices[day] + go(day + 1, True, trades + 1))
        return best

    return go(0, False, 0)


def max_alternating_sum(nums: list[int]) -> int:
    """Exercise 2 (LeetCode 1911): pick a subsequence; add elements at even positions, subtract at odd ones.
    Two states: the next pick is added (even) or subtracted (odd)."""
    even, odd = 0, 0
    for x in nums:
        even, odd = max(even, odd + x), max(odd, even - x)
    return even


def paint_fence(n: int, k: int) -> int:
    """Exercise 3 (LeetCode 276): n posts, k colours, never three in a row the same.
    States: last two posts same colour, or different."""
    if n == 0:
        return 0
    same, diff = 0, k
    for _ in range(n - 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff


if __name__ == "__main__":
    print(brute_trades([7, 1, 5, 3, 6, 4]), max_alternating_sum([4, 2, 5, 3]), paint_fence(3, 2))
