"""Volume 5, Chapter 14 - model solutions to the Thinking Problems (Section 14.14).

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations


def is_canonical(coins: list) -> tuple[bool, int | None]:
    """Thinking Problem 2: is largest-first always fewest for this coin set (which must contain 1)?
    By Kozen and Zaks, a failure, if any, lies below the sum of the two largest coins, S. Work out the true
    fewest coins and the greedy count for every amount below S, both from smaller amounts: O(n * S) time.
    Returns (True, None) or (False, the smallest failing amount)."""
    coins = sorted(set(coins))
    if not coins or coins[0] != 1:
        raise ValueError("the coin set must contain a 1")
    limit = coins[-1] + coins[-2] if len(coins) > 1 else 1
    best = [0] * limit
    greedy = [0] * limit
    big = 0                                            # index of the largest coin <= a
    for a in range(1, limit):
        while big + 1 < len(coins) and coins[big + 1] <= a:
            big += 1
        greedy[a] = 1 + greedy[a - coins[big]]
        best[a] = 1 + min(best[a - c] for c in coins if c <= a)
        if greedy[a] > best[a]:
            return False, a
    return True, None


if __name__ == "__main__":
    for cs in ([1, 2, 5, 10, 20, 50, 100, 200], [1, 3, 4], [1, 5], [1, 5, 8], [1, 7, 10], [1, 5, 12]):
        print(cs, is_canonical(cs))
