"""Volume 12, Chapter 4 - 1-D DP: Climbing Stairs, House Robber, Coin Change, Longest Increasing Subsequence.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

from bisect import bisect_left


def climb_stairs(n: int, steps: tuple[int, ...] = (1, 2)) -> int:
    """LeetCode 70 (generalised): ways to climb n stairs using the allowed step sizes. ways[i] = sum of ways[i - s]."""
    ways = [1] + [0] * n
    for i in range(1, n + 1):
        ways[i] = sum(ways[i - s] for s in steps if s <= i)
    return ways[n]


def house_robber(values: list[int]) -> int:
    """LeetCode 198: most value from houses in a row, never two neighbours. best[i] = max(skip, take)."""
    take, skip = 0, 0                       # best ending with house taken / not taken
    for v in values:
        take, skip = skip + v, max(take, skip)
    return max(take, skip)


def house_robber_circle(values: list[int]) -> int:
    """LeetCode 213: houses in a circle - the first and last are neighbours. Solve twice: without the last,
    and without the first."""
    if len(values) == 1:
        return values[0]
    return max(house_robber(values[:-1]), house_robber(values[1:]))


def coin_change_min(coins: list[int], amount: int) -> int:
    """LeetCode 322: fewest coins for an amount (-1 if impossible). fewest[a] = 1 + min(fewest[a - c])."""
    INF = amount + 1
    fewest = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and fewest[a - c] + 1 < fewest[a]:
                fewest[a] = fewest[a - c] + 1
    return fewest[amount] if fewest[amount] <= amount else -1


def coin_change_ways(coins: list[int], amount: int) -> int:
    """LeetCode 518: how many COMBINATIONS (order ignored) make the amount. Loop coins OUTSIDE so each
    combination is counted once, in coin order."""
    ways = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]


def lis_quadratic(values: list[int]) -> int:
    """LeetCode 300: longest strictly increasing subsequence. ending[i] = 1 + max ending[j] over j < i with smaller value."""
    ending = [1] * len(values)
    for i in range(len(values)):
        for j in range(i):
            if values[j] < values[i]:
                ending[i] = max(ending[i], ending[j] + 1)
    return max(ending, default=0)


def lis_fast(values: list[int]) -> int:
    """O(n log n): tails[k] = smallest possible last value of an increasing subsequence of length k + 1.
    Each new value replaces the first tail >= it (binary search, V5-C2)."""
    tails: list[int] = []
    for v in values:
        k = bisect_left(tails, v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v
    return len(tails)


def longest_growth_streak(monthly_users: list[int]) -> int:
    """Industry example: the longest run of months (not necessarily consecutive) with ever-growing user counts."""
    return lis_fast(monthly_users)


if __name__ == "__main__":
    print("stairs:", climb_stairs(10), climb_stairs(10, (1, 2, 3)))
    print("robber:", house_robber([2, 7, 9, 3, 1]), "| circle:", house_robber_circle([2, 3, 2]))
    print("coins 11 from 1,2,5:", coin_change_min([1, 2, 5], 11), "fewest;", coin_change_ways([1, 2, 5], 11), "ways")
    print("LIS:", lis_quadratic([10, 9, 2, 5, 3, 7, 101, 18]), lis_fast([10, 9, 2, 5, 3, 7, 101, 18]))
    print("growth streak:", longest_growth_streak([120, 90, 150, 140, 160, 130, 170, 200, 180]))
