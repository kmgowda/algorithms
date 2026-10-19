"""Volume 14, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from ch04_examples import extended_gcd, fast_power


def my_pow(x: float, n: int) -> float:
    """Exercise 1 (LeetCode 50): x^n for real x and any integer n, by repeated squaring."""
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result


def super_pow(a: int, digits: list[int]) -> int:
    """Exercise 2 (LeetCode 372): a^b mod 1337 where b is given as a list of digits.
    a^(10q + d) = (a^q)^10 x a^d - process digits left to right."""
    result = 1
    for d in digits:
        result = fast_power(result, 10, 1337) * fast_power(a, d, 1337) % 1337
    return result


def chinese_remainder(remainders: list[int], moduli: list[int]) -> int:
    """Exercise 3: the smallest x >= 0 with x = r_i (mod m_i) for pairwise coprime moduli."""
    x, m = 0, 1
    for r, mi in zip(remainders, moduli):
        g, p, _ = extended_gcd(m, mi)
        assert g == 1, "moduli must be pairwise coprime"
        x = (x + (r - x) * p % mi * m) % (m * mi)
        m *= mi
    return x


if __name__ == "__main__":
    print(my_pow(2.0, 10), my_pow(2.0, -2), super_pow(2, [1, 0]), chinese_remainder([2, 3, 2], [3, 5, 7]))
