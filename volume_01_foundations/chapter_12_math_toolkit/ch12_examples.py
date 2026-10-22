"""Volume 1, Chapter 12 - The Math Toolkit.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import math


def gauss_sum(n: int) -> int:
    """1 + 2 + ... + n = n(n + 1) / 2 (Figure 12.1)."""
    return n * (n + 1) // 2


def powers_of_two_sum(k: int) -> int:
    """1 + 2 + 4 + ... + 2^(k-1) = 2^k - 1 (Figure 12.2)."""
    return 2 ** k - 1


def geometric_sum(x: int, n: int) -> int:
    """1 + x + x^2 + ... + x^n = (x^(n+1) - 1) / (x - 1) for x != 1, and n + 1 when x = 1 (Section 12.5).
    n = -1 is the empty sum, 0."""
    if n < 0:
        return 0
    if x == 1:
        return n + 1
    return (x ** (n + 1) - 1) // (x - 1)


def log2_factorial(n: int) -> float:
    """log2(n!) = log2 1 + log2 2 + ... + log2 n, between (n/2) log2(n/2) and n log2 n (Figure 12.4)."""
    return sum(math.log2(k) for k in range(2, n + 1))


def harmonic(n: int) -> float:
    """H(n) = 1 + 1/2 + ... + 1/n, about ln n + 0.577 (Figure 12.6)."""
    return sum(1 / k for k in range(1, n + 1))


def harmonic_groups(n: int) -> list[float]:
    """The terms of H(n) grouped as [1], [1/2, 1/3], [1/4 .. 1/7], ...: each full group adds between
    1/2 and 1, and there are floor(log2 n) + 1 groups (Figure 12.6)."""
    groups, start = [], 1
    while start <= n:
        groups.append(sum(1 / k for k in range(start, min(2 * start, n + 1))))
        start *= 2
    return groups


def halving_total(start: int) -> int:
    """start + start//2 + start//4 + ... down to 1: less than 2 * start (Figure 12.5)."""
    total = 0
    while start >= 1:
        total += start
        start //= 2
    return total


def check_formulas(n: int) -> bool:
    """Compare the toolkit's formulas with direct sums for one n >= 1 (Figures 12.1, 12.2 and 12.7)."""
    gauss = sum(range(1, n + 1)) == n * (n + 1) // 2
    powers = sum(2 ** i for i in range(n)) == 2 ** n - 1
    halvings, m = 0, n
    while m > 1:
        m //= 2
        halvings += 1
    return gauss and powers and halvings == n.bit_length() - 1      # floor(log2 n)


if __name__ == "__main__":
    print(gauss_sum(10), gauss_sum(100), powers_of_two_sum(5), powers_of_two_sum(10), halving_total(1000))
    print(all(check_formulas(n) for n in range(1, 500)))
    print(geometric_sum(3, 4), round(log2_factorial(16), 2), round(harmonic(16), 4), len(harmonic_groups(16)))
