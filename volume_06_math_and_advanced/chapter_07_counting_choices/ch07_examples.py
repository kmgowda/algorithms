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


def pascal_mod(n: int, m: int) -> list:
    """Rows 0..n of Pascal's triangle modulo any m >= 1, prime or not: C(i, j) = C(i-1, j-1) + C(i-1, j) (Figure 7.3)."""
    if m < 1:
        raise ValueError("the modulus must be positive")
    rows = [[1 % m]]
    for i in range(1, n + 1):
        prev = rows[-1]
        rows.append([1 % m] + [(prev[j - 1] + prev[j]) % m for j in range(1, i)] + [1 % m])
    return rows


def lucas(n: int, k: int, p: int, log: list | None = None) -> int:
    """C(n, k) mod a prime p by Lucas's theorem: multiply C(n_i, k_i) over the base-p digits of n and k."""
    result = 1
    while n or k:
        ni, ki = n % p, k % p
        c = math.comb(ni, ki) if ki <= ni else 0
        if log is not None:
            log.append((ni, ki, c))
        result = result * c % p
        n, k = n // p, k // p
    return result


def derangements(n: int) -> int:
    """Orders of n books in which no book is in its own place, by inclusion-exclusion: sum of (-1)^i C(n, i) (n - i)!."""
    return sum((-1) ** i * math.comb(n, i) * math.factorial(n - i) for i in range(n + 1))


def derangements_by_listing(n: int) -> int:
    return sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))


def catalan(n: int) -> int:
    """The n-th Catalan number C(2n, n) / (n + 1): balanced bracket sequences with n pairs."""
    return math.comb(2 * n, n) // (n + 1)


def balanced_by_listing(n: int) -> int:
    count = 0
    for seq in itertools.product("()", repeat=2 * n):
        depth, ok = 0, True
        for ch in seq:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                ok = False
                break
        count += ok and depth == 0
    return count


def block_divisible(values: list, n: int) -> tuple[int, int] | None:
    """Pigeonhole: among any n whole numbers, some contiguous block values[i:j] sums to a multiple of n.
    The n + 1 prefix sums mod n take at most n values, so two are equal. Returns (i, j), or None if values is empty."""
    seen = {0: 0}
    total = 0
    for j, v in enumerate(values, start=1):
        total = (total + v) % n
        if total in seen:
            return seen[total], j
        seen[total] = j
    return None


if __name__ == "__main__":
    print(orders(5), arrangements(10, 3), choose(10, 3), choose(52, 5))
    print(choose_mod(1000, 500), choose(1000, 500) % P, len(str(choose(1000, 500))))
    print(with_repetition(3, 4), len([c for c in itertools.combinations_with_replacement("abc", 4)]))
    print(sum(choose(10, k) for k in range(11)), choose(10, 3) == choose(10, 7))
    print(pascal_mod(6, 4)[6], pascal_mod(6, 2)[4], [choose(6, j) for j in range(7)])
    log = []
    print(lucas(10, 3, 3, log), log, choose(10, 3) % 3, lucas(1000, 500, 13), choose(1000, 500) % 13)
    print([derangements(n) for n in range(7)], round(math.factorial(10) / math.e), derangements(10), derangements(10) / math.factorial(10))
    print([catalan(n) for n in range(8)], [balanced_by_listing(n) for n in range(6)])
    print(block_divisible([3, 1, 4, 1, 5, 9, 2], 7), choose(40, 6), choose(40, 20))
