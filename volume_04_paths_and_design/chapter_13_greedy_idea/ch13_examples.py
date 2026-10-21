"""Volume 4, Chapter 13 - The Greedy Idea: giving change with as few coins as possible.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

UK = [200, 100, 50, 20, 10, 5, 2, 1]                  # coins in pence, largest first
ODD = [4, 3, 1]                                       # an imaginary coin set where greed fails


def greedy_change(amount: int, coins: list) -> list:
    """Take the largest coin that fits, again and again (Figure 13.2)."""
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            out.append(c)
    if amount:
        raise ValueError("cannot make this amount with these coins")
    return out


def fewest_coins(amount: int, coins: list) -> list | None:
    """The true fewest coins, by checking every amount from 0 upwards (a preview of Volume 5)."""
    best: list = [[]] + [None] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] is not None and (best[a] is None or len(best[a - c]) + 1 < len(best[a])):
                best[a] = best[a - c] + [c]
    return best[amount]


def first_failure(coins: list, limit: int = 500) -> int | None:
    """The smallest amount for which greedy uses more coins than necessary."""
    for a in range(1, limit + 1):
        if len(greedy_change(a, coins)) != len(fewest_coins(a, coins)):
            return a
    return None


if __name__ == "__main__":
    print(greedy_change(87, UK), fewest_coins(87, UK))
    print(greedy_change(6, ODD), fewest_coins(6, ODD))
    print(first_failure(UK), first_failure(ODD), first_failure([25, 10, 1]), first_failure([50, 20, 10, 5, 2, 1]))
