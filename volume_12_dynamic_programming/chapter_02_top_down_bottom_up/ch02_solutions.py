"""Volume 12, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache


def stairs_top_down(n: int) -> int:
    """Exercise 1: ways to climb n stairs taking 1 or 2 at a time - top-down."""
    @lru_cache(maxsize=None)
    def ways(k: int) -> int:
        return 1 if k <= 1 else ways(k - 1) + ways(k - 2)
    return ways(n)


def stairs_bottom_up(n: int) -> int:
    """Exercise 1: the same, bottom-up."""
    dp = [1] * (n + 1)
    for k in range(2, n + 1):
        dp[k] = dp[k - 1] + dp[k - 2]
    return dp[n]


def min_cost_climbing(cost: list[int]) -> int:
    """Exercise 2 (LeetCode 746): pay cost[i] to stand on step i, climb 1 or 2; reach the top cheapest. Bottom-up."""
    n = len(cost)
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    return dp[n]


def fill_order(n: int) -> list[int]:
    """Exercise 3: the order a bottom-up table for 'fewest steps to 1' is filled - smallest first."""
    return list(range(1, n + 1))


if __name__ == "__main__":
    print(stairs_top_down(10), stairs_bottom_up(10), min_cost_climbing([10, 15, 20]),
          min_cost_climbing([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))
