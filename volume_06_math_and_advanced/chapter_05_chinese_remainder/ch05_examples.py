"""Volume 6, Chapter 5 - The Chinese Remainder Theorem: one number from its remainders.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import math


def crt(remainders: list, moduli: list) -> tuple[int | None, int]:
    """The smallest x >= 0 with x mod m_i = r_i for every i, and the combined modulus (Figure 5.2).
    Moduli need not be coprime; returns (None, lcm) when the remainders contradict each other."""
    x, m = 0, 1
    for r, n in zip(remainders, moduli):
        if n <= 0:
            raise ValueError("moduli must be positive")
        g = math.gcd(m, n)
        if (r - x) % g:
            return None, m * n // g
        # step from x by multiples of m until x mod n = r
        k = ((r - x) // g) * pow(m // g, -1, n // g) % (n // g)
        x += m * k
        m = m * n // g
        x %= m
    return x, m


def crt_by_search(remainders: list, moduli: list) -> int | None:
    m = math.lcm(*moduli) if moduli else 1
    return next((x for x in range(m) if all(x % n == r % n for r, n in zip(remainders, moduli))), None)


if __name__ == "__main__":
    print(crt([2, 3, 2], [3, 5, 7]), crt_by_search([2, 3, 2], [3, 5, 7]))
    print(crt([1, 2, 3, 4], [2, 3, 5, 7]), crt([3, 4], [6, 8]), crt([1, 2], [4, 6]))
