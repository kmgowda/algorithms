"""Volume 14, Chapter 4 - Number Theory II: Modular Arithmetic, Fast Power, Modular Inverse.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

MOD = 1_000_000_007


def mod_add(a: int, b: int, m: int = MOD) -> int:
    return (a + b) % m


def mod_mul(a: int, b: int, m: int = MOD) -> int:
    return a * b % m


def fast_power(base: int, exp: int, m: int = MOD) -> int:
    """base^exp mod m by repeated squaring (V2-C9): read exp's bits; square each step, multiply on a 1-bit.
    O(log exp) multiplications instead of exp."""
    result, base = 1, base % m
    while exp:
        if exp & 1:
            result = result * base % m
        base = base * base % m
        exp >>= 1
    return result


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b) - Euclid, keeping track of the coefficients."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def mod_inverse(a: int, m: int) -> int:
    """The x with a*x = 1 (mod m), which exists exactly when gcd(a, m) = 1. Raises ValueError otherwise."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return x % m


def mod_inverse_prime(a: int, p: int) -> int:
    """Fermat's little theorem: for prime p, a^(p-1) = 1, so a^(p-2) is the inverse."""
    return fast_power(a, p - 2, p)


def day_of_week(start_day: int, days_later: int) -> int:
    """Beginner example: weekdays are arithmetic mod 7 (0 = Monday)."""
    return (start_day + days_later) % 7


def isbn10_valid(isbn: str) -> bool:
    """Industry example: ISBN-10 check digit - sum of (position x digit) must be divisible by 11 ('X' = 10)."""
    chars = isbn.replace("-", "")
    if len(chars) != 10:
        return False
    total = 0
    for i, ch in enumerate(chars, 1):
        value = 10 if ch == "X" and i == 10 else int(ch) if ch.isdigit() else None
        if value is None:
            return False
        total += i * value
    return total % 11 == 0


if __name__ == "__main__":
    print(mod_add(MOD - 1, 5), mod_mul(10 ** 9, 10 ** 9), fast_power(2, 10), fast_power(3, 10 ** 18))
    print(extended_gcd(240, 46), mod_inverse(3, 11), mod_inverse_prime(3, 11), 3 * mod_inverse(3, 11) % 11)
    print("100 days after a Monday is day", day_of_week(0, 100), "(0 = Monday)")
    print(isbn10_valid("0-306-40615-2"), isbn10_valid("0-306-40615-3"))
