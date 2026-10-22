"""Volume 6, Chapter 8 - model solutions to the Thinking Problems (Section 8.13)."""

from __future__ import annotations


def broken_stairs(n: int, broken: set) -> int:
    """Ways to climb n stairs one or two at a time without standing on a broken stair. O(n) time:
    each stair's count is found once, from the two below it."""
    if n in broken:
        return 0
    ways = [0] * (n + 1)
    ways[0] = 1
    for k in range(1, n + 1):
        if k not in broken:
            ways[k] = ways[k - 1] + (ways[k - 2] if k >= 2 else 0)
    return ways[n]


def ways_coins(amount: int, coins: list, key_on_amount_only: bool = False) -> int:
    """Ways to make amount from coins, order ignored: use coin i again, or move on to the next coin.
    key_on_amount_only=True is Thinking Problem 3's bug: the memo forgets which coins are still allowed."""
    memo = {}

    def go(i, a):
        if a == 0:
            return 1
        if a < 0 or i == len(coins):
            return 0
        key = a if key_on_amount_only else (i, a)
        if key not in memo:
            memo[key] = go(i, a - coins[i]) + go(i + 1, a)
        return memo[key]

    return go(0, amount)
