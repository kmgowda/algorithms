"""Volume 6, Chapter 13 - Thinking Problems.

Problem 1: with the coins in the outer loop, after j coins ways[a] counts the sets that use only those j coins (checked).
Problem 2: at most one book of each price: the same table, but each amount loop runs downwards.
Problem 3: a coin worth 0 used to double the table silently (count_sets(3, [0, 1]) gave 2); it is now refused.
"""

from __future__ import annotations

import itertools


def sets_after(amount: int, coins: list, j: int) -> list:
    ways = [1] + [0] * amount
    for c in coins[:j]:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways


def count_distinct(amount: int, prices: list) -> int:
    """Ways to pick a subset of the books (each at most once) costing exactly amount."""
    ways = [1] + [0] * amount
    for p in prices:
        for a in range(amount, p - 1, -1):          # downwards: each book is used at most once
            ways[a] += ways[a - p]
    return ways[amount]


def brute_distinct(amount: int, prices: list) -> int:
    return sum(1 for k in range(len(prices) + 1) for c in itertools.combinations(prices, k) if sum(c) == amount)


if __name__ == "__main__":
    from ch13_examples import COINS, count_sets
    print(sets_after(10, COINS, 2), count_sets(10, COINS)[0], count_distinct(10, [2, 3, 5, 5, 7]))
