"""Volume 6, Chapter 11 - Big Numbers and Floating Point: what computer numbers can and cannot hold.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import math
from fractions import Fraction


def wrap(n: int, bits: int = 8) -> int:
    """What an n-bit signed (two's complement) register holds after storing n (Figure 11.1)."""
    n &= (1 << bits) - 1
    return n - (1 << bits) if n >= 1 << (bits - 1) else n


def add_tenths(times: int) -> float:
    total = 0.0
    for _ in range(times):
        total += 0.1
    return total


def naive_sum(values: list) -> float:
    total = 0.0
    for v in values:
        total += v
    return total


def kahan_sum(values: list) -> float:
    """Compensated summation (Figure 11.3): carry the rounding error forward."""
    total, lost = 0.0, 0.0
    for v in values:
        y = v - lost
        t = total + y
        lost = (t - total) - y
        total = t
    return total


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


if __name__ == "__main__":
    print(wrap(127), wrap(128), wrap(200), wrap(-1), wrap(300), 2 ** 100)
    print(0.1 + 0.2, 0.1 + 0.2 == 0.3, close(0.1 + 0.2, 0.3), add_tenths(10), add_tenths(10) == 1.0)
    big = [1e16] + [1.0] * 10000
    print(naive_sum(big) - 1e16, kahan_sum(big) - 1e16, math.fsum(big) - 1e16)
    print(2.0 ** 53 + 1 == 2.0 ** 53, Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10), 1e308 * 10, float("inf") - float("inf"))
