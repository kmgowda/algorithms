"""Volume 6, Chapter 1 - Divisibility and Euclid: divisors, the greatest common divisor, and the least common multiple.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import math


def divisors(n: int) -> list:
    """Every divisor of n, found by checking up to the square root (Figure 1.2): divisors come in pairs d, n // d."""
    if n <= 0:
        raise ValueError("divisors are defined here for positive whole numbers")
    small, large, d = [], [], 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def gcd_by_listing(a: int, b: int) -> int:
    common = set(divisors(a)) & set(divisors(b))
    return max(common)


def gcd(a: int, b: int, log: list | None = None) -> int:
    """Euclid (Figure 1.3): gcd(a, b) = gcd(b, a mod b), until b is 0."""
    a, b = abs(a), abs(b)
    while b:
        if log is not None:
            log.append((a, b, a % b))
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple: a * b / gcd(a, b); 0 if either is 0."""
    return 0 if a == 0 or b == 0 else abs(a * b) // gcd(a, b)


def euclid_steps(a: int, b: int) -> int:
    log = []
    gcd(a, b, log)
    return len(log)


if __name__ == "__main__":
    print(divisors(36), divisors(84), gcd_by_listing(84, 36))
    log = []
    print(gcd(84, 36, log), log, lcm(84, 36))
    print(gcd(1071, 462), euclid_steps(1071, 462), euclid_steps(832040, 514229), gcd(2 ** 61 - 1, 10 ** 18))
