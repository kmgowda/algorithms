"""Volume 14, Chapter 6 - Combinatorics and Counting.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

MOD = 1_000_000_007


def permutations_count(n: int, k: int) -> int:
    """Ordered arrangements of k items from n: n x (n-1) x ... x (n-k+1)."""
    out = 1
    for i in range(k):
        out *= n - i
    return out


def combinations_count(n: int, k: int) -> int:
    """Unordered choices: C(n, k) = n! / (k! (n-k)!), built step by step so every division is exact."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    out = 1
    for i in range(1, k + 1):
        out = out * (n - k + i) // i
    return out


def pascal_rows(n: int) -> list[list[int]]:
    """LeetCode 118: each entry is the sum of the two above it - C(n, k) = C(n-1, k-1) + C(n-1, k)."""
    rows = [[1]]
    for _ in range(n - 1):
        prev = rows[-1]
        rows.append([1] + [a + b for a, b in zip(prev, prev[1:])] + [1])
    return rows


class BinomialMod:
    """C(n, k) mod a prime for many queries: precompute factorials and their inverses (Chapter 4) once."""

    def __init__(self, limit: int, p: int = MOD) -> None:
        self.p = p
        self.fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            self.fact[i] = self.fact[i - 1] * i % p
        self.inv = [1] * (limit + 1)
        self.inv[limit] = pow(self.fact[limit], p - 2, p)
        for i in range(limit, 0, -1):
            self.inv[i - 1] = self.inv[i] * i % p

    def choose(self, n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return self.fact[n] * self.inv[k] % self.p * self.inv[n - k] % self.p


def catalan(n: int) -> int:
    """Catalan numbers C(2n, n) / (n + 1): balanced bracket strings, BST shapes (LeetCode 96), triangulations..."""
    return combinations_count(2 * n, n) // (n + 1)


def stars_and_bars(items: int, boxes: int) -> int:
    """Ways to put identical items into distinct boxes (boxes may be empty): C(items + boxes - 1, boxes - 1)."""
    return combinations_count(items + boxes - 1, boxes - 1)


def lottery_odds(pool: int, picks: int) -> int:
    """Industry example: a lottery drawing 6 of 49 numbers - the number of possible tickets."""
    return combinations_count(pool, picks)


def password_space(length: int, alphabet: int) -> int:
    """Industry example: passwords of a given length over an alphabet - ordered, repetition allowed."""
    return alphabet ** length


if __name__ == "__main__":
    print(permutations_count(10, 3), combinations_count(10, 3), pascal_rows(5))
    bm = BinomialMod(10 ** 6)
    print(bm.choose(10, 3), bm.choose(10 ** 6, 500000))
    print([catalan(n) for n in range(8)], stars_and_bars(5, 3))
    print("6 of 49 lottery:", lottery_odds(49, 6), "| 8-char passwords over 62 symbols:", password_space(8, 62))
