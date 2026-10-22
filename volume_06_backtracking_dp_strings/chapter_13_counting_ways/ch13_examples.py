"""Volume 6, Chapter 13 - Counting the Ways: how many ways, and the loop order that decides what "way" means.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import itertools

COINS = [1, 2, 5]


def count_sets(amount: int, coins: list) -> tuple[int, list]:
    """Ways to make amount where order does not matter (coins outer loop) (Figure 13.2). Returns (ways, table)."""
    if any(c <= 0 for c in coins):
        raise ValueError("every coin must be worth at least 1")
    ways = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount], ways


def count_orders(amount: int, coins: list) -> tuple[int, list]:
    """Ways where order matters (amount outer loop): 1+2 and 2+1 count separately (Section 13.5)."""
    if any(c <= 0 for c in coins):
        raise ValueError("every coin must be worth at least 1")
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
    """Ways to read a string of digits as letters A=1 ... Z=26 (Section 13.8): one digit or two at a time."""
    n = len(message)
    ways = [1] + [0] * n
    for i in range(1, n + 1):
        if message[i - 1] != "0":
            ways[i] += ways[i - 1]
        if i >= 2 and message[i - 2] != "0" and 10 <= int(message[i - 2:i]) <= 26:
            ways[i] += ways[i - 2]
    return ways[n]


def free_digit_table(length: int, total: int) -> list:
    """F[r][t] = ways to write r free digits (0-9, leading zeros allowed) adding up to t (Section 13.6)."""
    f = [[0] * (total + 1) for _ in range(length + 1)]
    f[0][0] = 1
    for r in range(1, length + 1):
        for t in range(total + 1):
            f[r][t] = sum(f[r - 1][t - d] for d in range(10) if d <= t)
    return f


def count_digit_sum(limit: int, s: int) -> tuple[int, list]:
    """Digit DP: how many numbers from 0 to limit have digits adding up to s (Section 13.6).
    Walk the digits of limit from the left; at each position every smaller digit frees the rest, counted by
    the table F; then keep the limit's own digit ("tight") and move on. Returns (count, the walk's additions)."""
    if limit < 0 or s < 0:
        return 0, []
    digits = [int(c) for c in str(limit)]
    f = free_digit_table(len(digits), s)
    count, so_far, steps = 0, 0, []
    for pos, top in enumerate(digits):
        rest = len(digits) - pos - 1
        for d in range(top):
            need = s - so_far - d
            if 0 <= need:
                add = f[rest][need]
                if add:
                    steps.append((pos, d, rest, need, add))
                count += add
        so_far += top
    if so_far == s:
        count += 1
        steps.append(("limit itself", limit))
    return count, steps


if __name__ == "__main__":
    print(count_sets(10, COINS), count_orders(10, COINS)[0], brute_sets(10, COINS))
    print(count_sets(100, [1, 2, 5, 10, 20, 50, 100])[0], count_sets(200, [1, 2, 5, 10, 20, 50, 100, 200])[0])
    print(count_sets(4, [1, 2])[0], count_orders(4, [1, 2])[0])
    print([decodings(m) for m in ("12", "226", "2101", "10", "0", "", "1111111111", "301")])
