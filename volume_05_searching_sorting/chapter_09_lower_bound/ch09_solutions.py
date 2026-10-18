"""Volume 5, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

import math


def min_and_max(values: list[int]) -> tuple[int, int, int]:
    """Exercise 1: smallest and largest with about 3n/2 comparisons (pairs first), not 2n. Returns (min, max, comparisons)."""
    comparisons = 0
    if not values:
        raise ValueError("empty")
    if len(values) % 2:
        lo = hi = values[0]
        start = 1
    else:
        comparisons += 1
        lo, hi = (values[0], values[1]) if values[0] < values[1] else (values[1], values[0])
        start = 2
    for i in range(start, len(values), 2):
        a, b = values[i], values[i + 1]
        comparisons += 1
        small, big = (a, b) if a < b else (b, a)
        comparisons += 2
        lo, hi = min(lo, small), max(hi, big)
    return lo, hi, comparisons


def tournament_rounds_to_rank(teams: int) -> int:
    """Exercise 2: matches needed (at least) to fully rank `teams` teams by pairwise games = ceil(log2(teams!))."""
    return math.ceil(math.log2(math.factorial(teams))) if teams > 1 else 0


def weighings_for_fake_coin(coins: int) -> int:
    """Exercise 3: a balance scale has THREE outcomes (left, right, equal), so k weighings separate 3^k cases.
    Finding one lighter fake among `coins` needs ceil(log3(coins)) weighings."""
    k = 0
    while 3 ** k < coins:
        k += 1
    return k


if __name__ == "__main__":
    print(min_and_max([7, 2, 9, 4, 3, 8]), tournament_rounds_to_rank(8), weighings_for_fake_coin(9), weighings_for_fake_coin(10))
