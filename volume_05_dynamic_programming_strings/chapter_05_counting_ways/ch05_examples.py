"""Volume 5, Chapter 5 - Counting the Ways: how many ways, and the loop order that decides what "way" means.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import itertools

COINS = [1, 2, 5]


def count_sets(amount: int, coins: list) -> tuple[int, list]:
    """Ways to make amount where order does not matter (coins outer loop) (Figure 5.2). Returns (ways, table)."""
    ways = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount], ways


def count_orders(amount: int, coins: list) -> tuple[int, list]:
    """Ways where order matters (amount outer loop): 1+2 and 2+1 count separately (Figure 5.3)."""
    ways = [1] + [0] * amount
    for a in range(1, amount + 1):
        ways[a] = sum(ways[a - c] for c in coins if c <= a)
    return ways[amount], ways


def brute_sets(amount: int, coins: list) -> int:
    count = 0
    for counts in itertools.product(*[range(amount // c + 1) for c in coins]):
        if sum(k * c for k, c in zip(counts, coins)) == amount:
            count += 1
    return count


def decodings(message: str) -> int:
    """Ways to read a string of digits as letters A=1 ... Z=26 (Section 5.7): one digit or two at a time."""
    n = len(message)
    ways = [1] + [0] * n
    for i in range(1, n + 1):
        if message[i - 1] != "0":
            ways[i] += ways[i - 1]
        if i >= 2 and message[i - 2] != "0" and 10 <= int(message[i - 2:i]) <= 26:
            ways[i] += ways[i - 2]
    return ways[n]


if __name__ == "__main__":
    print(count_sets(10, COINS), count_orders(10, COINS)[0], brute_sets(10, COINS))
    print(count_sets(100, [1, 2, 5, 10, 20, 50, 100])[0], count_sets(200, [1, 2, 5, 10, 20, 50, 100, 200])[0])
    print(count_sets(4, [1, 2])[0], count_orders(4, [1, 2])[0])
    print([decodings(m) for m in ("12", "226", "2101", "10", "0", "", "1111111111", "301")])
