"""Volume 6, Chapter 7 - Counting Choices: factorials, combinations, and counting modulo a prime.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import itertools
import math

P = 1_000_000_007                                     # a prime, so every non-zero number has an inverse


def orders(n: int) -> int:
    """Ways to line up n books: n!."""
    return math.factorial(n)


def arrangements(n: int, k: int) -> int:
    """Ways to fill k places in order from n books: n! / (n - k)!."""
    return math.perm(n, k)


def choose(n: int, k: int) -> int:
    """Ways to pick k of n when order does not matter: n! / (k! (n - k)!) (Figure 7.2)."""
    return math.comb(n, k)


def choose_mod(n: int, k: int, p: int = P) -> int:
    """C(n, k) mod p using factorials and the inverse of k! (n - k)! (Chapter 4)."""
    if k < 0 or k > n:
        return 0
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p
    return fact[n] * pow(fact[k] * fact[n - k] % p, p - 2, p) % p


def with_repetition(n: int, k: int) -> int:
    """Ways to pick k items from n kinds when kinds may repeat (stars and bars): C(n + k - 1, k)."""
    return math.comb(n + k - 1, k) if n > 0 else (1 if k == 0 else 0)


if __name__ == "__main__":
    print(orders(5), arrangements(10, 3), choose(10, 3), choose(52, 5))
    print(choose_mod(1000, 500), choose(1000, 500) % P, len(str(choose(1000, 500))))
    print(with_repetition(3, 4), len([c for c in itertools.combinations_with_replacement("abc", 4)]))
    print(sum(choose(10, k) for k in range(11)), choose(10, 3) == choose(10, 7))
