"""Volume 5, Chapter 18 - Thinking Problems.

Problem 1: greedy cover's first pick covers at least |U| / OPT items (checked on random instances).
Problem 2: is "largest coin first" always best for a coin set? Compare with exact counts up to a limit.
Problem 3: coins 1, 3, 4: greedy pays 6 with three coins (4 + 1 + 1), the best is two (3 + 3).
"""

from __future__ import annotations

import math


def greedy_change(coins: list, amount: int) -> list:
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            out.append(c)
            amount -= c
    return out if amount == 0 else None


def fewest_coins(coins: list, limit: int) -> list:
    best = [0] + [math.inf] * limit
    for a in range(1, limit + 1):
        best[a] = min((best[a - c] + 1 for c in coins if c <= a), default=math.inf)
    return best


def greedy_always_best(coins: list, limit: int) -> int | None:
    """The smallest amount up to limit where largest-first uses more coins than necessary, or None."""
    best = fewest_coins(coins, limit)
    for a in range(1, limit + 1):
        g = greedy_change(coins, a)
        if best[a] < math.inf and (g is None or len(g) > best[a]):
            return a
    return None


if __name__ == "__main__":
    print(greedy_change([1, 3, 4], 6), fewest_coins([1, 3, 4], 6)[6])
    print(greedy_always_best([1, 2, 5, 10, 20, 50, 100, 200], 1000), greedy_always_best([1, 3, 4], 100), greedy_always_best([1, 10, 25], 100))
