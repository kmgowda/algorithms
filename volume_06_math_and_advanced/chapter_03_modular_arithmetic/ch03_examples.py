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


if __name__ == "__main__":
    print(clock(9, 5), clock(11, 25), clock(3, -5))
    print(last_digit_table(7), last_digit_table(3))
    print(power_mod_naive(7, 100, 10), power_mod(7, 100, 10), power_mod(3, 1000, 1000007), pow(3, 1000, 1000007))
    print(power_mod(2, 10 ** 18, 10 ** 9 + 7), pow(2, 10 ** 18, 10 ** 9 + 7))
