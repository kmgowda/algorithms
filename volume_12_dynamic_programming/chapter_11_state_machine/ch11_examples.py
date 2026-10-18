"""Volume 12, Chapter 11 - State Machine DP: Stock Trading Problems.

Each day you are in one of a few STATES (holding a share, not holding, cooling down). The DP keeps the best
money for each state and moves between states day by day.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import math


def one_trade(prices: list[int]) -> int:
    """LeetCode 121: buy once, sell once later. Track the cheapest buy so far."""
    cheapest, best = math.inf, 0
    for p in prices:
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
    return best


def unlimited_trades(prices: list[int]) -> int:
    """LeetCode 122: any number of trades, one share at a time.
    States: hold (own a share) and free (own nothing)."""
    hold, free = -math.inf, 0
    for p in prices:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free


def k_trades(prices: list[int], k: int) -> int:
    """LeetCode 123 / 188: at most k complete trades. States: (trades started so far, holding or not)."""
    hold = [-math.inf] * (k + 1)                # hold[j]: holding, j-th buy made
    free = [0] * (k + 1)                        # free[j]: not holding, j trades completed
    for p in prices:
        for j in range(1, k + 1):
            hold[j] = max(hold[j], free[j - 1] - p)
            free[j] = max(free[j], hold[j] + p)
    return free[k]


def with_cooldown(prices: list[int]) -> int:
    """LeetCode 309: after selling you must rest one day. States: hold, sold (just sold today), rest."""
    hold, sold, rest = -math.inf, 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)


def with_fee(prices: list[int], fee: int) -> int:
    """LeetCode 714 (industry: brokerage fees): every completed trade pays a fee."""
    hold, free = -math.inf, 0
    for p in prices:
        hold, free = max(hold, free - p), max(free, hold + p - fee)
    return free


if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]
    print("one trade:", one_trade(prices), "| unlimited:", unlimited_trades(prices))
    print("two trades:", k_trades([3, 3, 5, 0, 0, 3, 1, 4], 2), "| cooldown:", with_cooldown([1, 2, 3, 0, 2]))
    print("with a fee of 2:", with_fee([1, 3, 2, 8, 4, 9], 2))
