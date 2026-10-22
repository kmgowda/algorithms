"""Volume 6, Chapter 3 - Modular Arithmetic and Fast Powers: clock arithmetic, and huge powers in a few steps.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations


def clock(hour: int, add: int, size: int = 12) -> int:
    """Clock arithmetic: the hour after adding, on a clock of the given size (Figure 3.1)."""
    return (hour + add) % size


def power_mod_naive(base: int, exp: int, mod: int) -> tuple[int, int]:
    """Multiply exp times, reducing each time. Returns (result, multiplications)."""
    result, count = 1 % mod, 0
    for _ in range(exp):
        result = result * base % mod
        count += 1
    return result, count


def power_mod(base: int, exp: int, mod: int) -> tuple[int, int]:
    """Square-and-multiply (Figure 3.3): read the bits of exp from the right. Returns (result, multiplications)."""
    if mod <= 0:
        raise ValueError("the modulus must be positive")
    if exp < 0:
        raise ValueError("negative powers need an inverse (Chapter 4)")
    result, square, count = 1 % mod, base % mod, 0
    while exp:
        if exp & 1:
            result = result * square % mod
            count += 1
        exp >>= 1
        if exp:
            square = square * square % mod
            count += 1
    return result, count


def last_digit_table(base: int, n: int = 8) -> list:
    """Last digits of base^1 .. base^n: they repeat (Figure 3.2)."""
    return [pow(base, k, 10) for k in range(1, n + 1)]


def power_mod_trace(base: int, exp: int, mod: int) -> list:
    """Square-and-multiply with its trace (Figure 3.4): rows (bit, square before the step, result after the step)."""
    rows, result, square = [], 1 % mod, base % mod
    while exp:
        bit = exp & 1
        if bit:
            result = result * square % mod
        rows.append((bit, square, result))
        exp >>= 1
        if exp:
            square = square * square % mod
    return rows


def residue_row(a: int, p: int) -> list:
    """a x 1, a x 2, ..., a x (p - 1) mod p: for a prime p not dividing a, a rearrangement of 1..p-1 (Figure 3.3)."""
    return [a * k % p for k in range(1, p)]


def phi(n: int) -> int:
    """Euler's phi: how many of 1..n are coprime to n, from the prime factors: n x product of (1 - 1/p)."""
    if n < 1:
        raise ValueError("phi needs a positive whole number")
    result, m, d = n, n, 2
    while d * d <= m:
        if m % d == 0:
            while m % d == 0:
                m //= d
            result -= result // d
        d += 1
    if m > 1:
        result -= result // m
    return result


def phi_by_counting(n: int) -> int:
    from math import gcd
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def mul_mod_by_doubling(a: int, b: int, m: int) -> int:
    """a x b mod m without ever forming a number above 2m: add a, doubled, for each 1 bit of b ("Russian peasant")."""
    a, result = a % m, 0
    while b:
        if b & 1:
            result = (result + a) % m
        a = (a + a) % m
        b >>= 1
    return result


def average_multiplications(lo: int, hi: int) -> float:
    return sum(power_mod(3, e, 1_000_003)[1] for e in range(lo, hi)) / (hi - lo)


if __name__ == "__main__":
    print(clock(9, 5), clock(11, 25), clock(3, -5))
    print(last_digit_table(7), last_digit_table(3))
    print(power_mod_naive(7, 100, 10), power_mod(7, 100, 10), power_mod(3, 1000, 1000007), pow(3, 1000, 1000007))
    print(power_mod(2, 10 ** 18, 10 ** 9 + 7), pow(2, 10 ** 18, 10 ** 9 + 7))
    print(power_mod_trace(3, 13, 7), power_mod_trace(7, 100, 10))
    print(residue_row(3, 7), sorted(residue_row(3, 7)), residue_row(2, 6))
    print(phi(3233), phi(12), phi(7), phi(1), phi_by_counting(12), pow(5, phi(12), 12), pow(10, 6, 7))
    print(round(average_multiplications(1_000_000, 1_001_000), 1), (10 ** 9 + 7) ** 2 < 2 ** 63, (2 ** 62 + 1) ** 2 < 2 ** 63)
    print(mul_mod_by_doubling(2 ** 62 + 5, 2 ** 62 + 9, 2 ** 62 + 11), (2 ** 62 + 5) * (2 ** 62 + 9) % (2 ** 62 + 11))
