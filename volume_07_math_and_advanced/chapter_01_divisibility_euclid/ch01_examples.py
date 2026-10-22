"""Volume 7, Chapter 1 - Divisibility and Euclid: divisors, the greatest common divisor, and the least common multiple.

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
    """Least common multiple: a / gcd(a, b) * b, dividing first so no intermediate exceeds the answer; 0 if either is 0."""
    return 0 if a == 0 or b == 0 else abs(a) // gcd(a, b) * abs(b)


def gcd_recursive(a: int, b: int) -> int:
    """The same rule written recursively: gcd(a, 0) = a, otherwise gcd(b, a mod b)."""
    a, b = abs(a), abs(b)
    return a if b == 0 else gcd_recursive(b, a % b)


def gcd_many(values: list) -> int:
    """gcd of a list, folded pairwise; the gcd of nothing is 0 (0 is divisible by everything)."""
    g = 0
    for v in values:
        g = gcd(g, v)
    return g


def lcm_many(values: list) -> int:
    m = 1
    for v in values:
        m = lcm(m, v)
    return m


def tiling(a: int, b: int) -> list:
    """Euclid as tiling an a-by-b rectangle with squares (Figure 1.3): a list of (square side, how many squares)."""
    a, b = abs(a), abs(b)
    out = []
    while b:
        out.append((b, a // b))
        a, b = b, a % b
    return out


def fibonacci(k: int) -> int:
    x, y = 0, 1
    for _ in range(k):
        x, y = y, x + y
    return x


def worst_pair_below(limit: int) -> tuple:
    """(steps, a, b): the pair with b <= a < limit that makes Euclid take the most steps (Lamé: a Fibonacci pair)."""
    best = (0, 0, 0)
    for a in range(1, limit):
        for b in range(1, a + 1):
            s = euclid_steps(a, b)
            if s > best[0]:
                best = (s, a, b)
    return best


def lame_bound(b: int) -> float:
    """Lamé: Euclid on (a, b) with a > b >= 1 takes at most log_phi(b) + 1 steps, about 1.44 log2(b) + 1."""
    phi = (1 + 5 ** 0.5) / 2
    return math.log(b, phi) + 1


def euclid_steps(a: int, b: int) -> int:
    log = []
    gcd(a, b, log)
    return len(log)


if __name__ == "__main__":
    print(divisors(36), divisors(84), gcd_by_listing(84, 36))
    log = []
    print(gcd(84, 36, log), log, lcm(84, 36))
    print(gcd(1071, 462), euclid_steps(1071, 462), euclid_steps(832040, 514229), gcd(2 ** 61 - 1, 10 ** 18))
    print(tiling(84, 36), tiling(1071, 462), tiling(21, 13), fibonacci(29), fibonacci(30))
    print(worst_pair_below(1000), round(lame_bound(514229), 2), round(lame_bound(610), 2))
    print(gcd_many([84, 36, 60]), lcm_many([12, 18, 30]), gcd_many([]), lcm(2 ** 40, 3 ** 30) == 2 ** 40 * 3 ** 30)
