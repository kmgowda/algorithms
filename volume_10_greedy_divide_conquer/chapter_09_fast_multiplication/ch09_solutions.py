"""Volume 10, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

import math


def multiplications_needed(n: int, method: str) -> int:
    """Exercise 1: single-digit multiplications for n-digit numbers (n a power of two, no cutoff)."""
    if n == 1:
        return 1
    return (4 if method == "four" else 3) * multiplications_needed(n // 2, method)


def karatsuba_int(x: int, y: int) -> int:
    """Exercise 2: Karatsuba on Python ints, splitting by powers of ten."""
    if x < 10 or y < 10:
        return x * y
    m = max(len(str(x)), len(str(y))) // 2
    p = 10 ** m
    x1, x0 = divmod(x, p)
    y1, y0 = divmod(y, p)
    high = karatsuba_int(x1, y1)
    low = karatsuba_int(x0, y0)
    middle = karatsuba_int(x1 + x0, y1 + y0) - high - low
    return high * p * p + middle * p + low


def complex_multiply_three(a: int, b: int, c: int, d: int) -> tuple[int, int]:
    """Exercise 3 (Gauss's trick, the idea behind Karatsuba): (a + bi)(c + di) with 3 real multiplications."""
    k1 = c * (a + b)
    k2 = a * (d - c)
    k3 = b * (c + d)
    return k1 - k3, k1 + k2


def exponent(a: int, b: int) -> float:
    """Exercise 4: the exponent log_b(a) in O(n^log_b(a)) for 'a subproblems of size n/b'."""
    return math.log(a, b)


if __name__ == "__main__":
    print(multiplications_needed(1024, "four"), multiplications_needed(1024, "three"))
    print(karatsuba_int(1234, 5678), complex_multiply_three(1, 2, 3, 4), round(exponent(3, 2), 3), round(exponent(7, 2), 3))
