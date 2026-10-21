"""Volume 6, Chapter 4 - Inverses and the Extended Euclid: undoing multiplication on a clock.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations


def extended_gcd(a: int, b: int, log: list | None = None) -> tuple[int, int, int]:
    """Returns (g, x, y) with a*x + b*y = g = gcd(a, b) (Figure 4.2)."""
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x, y = extended_gcd(b, a % b, log)
    if log is not None:
        log.append((a, b, x, y))
    return g, y, x - (a // b) * y


def inverse(a: int, m: int) -> int | None:
    """The number x with a*x mod m = 1, or None when gcd(a, m) is not 1 (Figure 4.3)."""
    if m <= 0:
        raise ValueError("the modulus must be positive")
    g, x, _ = extended_gcd(a % m, m)
    return x % m if g == 1 else None


def inverse_by_search(a: int, m: int) -> int | None:
    return next((x for x in range(m) if a * x % m == 1), None)


def solve_linear(a: int, b: int, m: int) -> list:
    """Every x in 0..m-1 with a*x mod m = b."""
    return [x for x in range(m) if a * x % m == b % m]


if __name__ == "__main__":
    print(extended_gcd(84, 36), extended_gcd(240, 46))
    print(inverse(3, 7), inverse(7, 26), inverse(4, 8), inverse(17, 3120), pow(17, -1, 3120))
    print(solve_linear(3, 2, 7), solve_linear(4, 2, 8), solve_linear(4, 3, 8))
