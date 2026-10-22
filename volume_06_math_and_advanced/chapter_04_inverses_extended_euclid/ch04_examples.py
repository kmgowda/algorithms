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


def extended_gcd_table(a: int, b: int) -> list:
    """Iterative extended Euclid (Figure 4.3): rows (r, s, t, q) with r = a*s + b*t at every row;
    each new row is the row two above minus q times the row above. The last nonzero r is the gcd."""
    rows = [(a, 1, 0, None), (b, 0, 1, None)]
    while rows[-1][0] != 0:
        (r0, s0, t0, _), (r1, s1, t1, _) = rows[-2], rows[-1]
        q = r0 // r1
        rows[-1] = (r1, s1, t1, q)
        rows.append((r0 - q * r1, s0 - q * s1, t0 - q * t1, None))
    return rows


def extended_gcd_iterative(a: int, b: int) -> tuple[int, int, int]:
    rows = extended_gcd_table(abs(a), abs(b))
    r, s, t, _ = rows[-2]
    return r, s * (1 if a >= 0 else -1), t * (1 if b >= 0 else -1)


def smallest_positive_combination(a: int, b: int, bound: int = 60) -> int:
    """Bezout by brute force: the smallest positive a*x + b*y over small x, y (it equals gcd(a, b))."""
    return min(v for x in range(-bound, bound + 1) for y in range(-bound, bound + 1) if (v := a * x + b * y) > 0)


def solve_congruence(a: int, b: int, m: int) -> tuple[int, int, int] | None:
    """All solutions of a*x = b (mod m): None if gcd(a, m) does not divide b, otherwise (x0, step, count),
    meaning x = x0, x0 + step, ..., count = gcd(a, m) solutions in 0..m-1, step = m / gcd."""
    if m <= 0:
        raise ValueError("the modulus must be positive")
    g, x, _ = extended_gcd(a % m, m)
    if b % g:
        return None
    step = m // g
    x0 = x * (b // g) % step
    return x0, step, g


def inverses_up_to(p: int) -> list:
    """Inverses of 1..p-1 modulo a prime p in O(p): inv[i] = -(p // i) * inv[p mod i] mod p."""
    inv = [0, 1] + [0] * (p - 2)
    for i in range(2, p):
        inv[i] = (p - (p // i) * inv[p % i] % p) % p
    return inv


def inverse_by_fermat(a: int, p: int) -> int:
    """For a prime p not dividing a: a^(p - 2) mod p (Fermat, Chapter 3)."""
    return pow(a, p - 2, p)


if __name__ == "__main__":
    print(extended_gcd(84, 36), extended_gcd(240, 46))
    print(inverse(3, 7), inverse(7, 26), inverse(4, 8), inverse(17, 3120), pow(17, -1, 3120))
    print(solve_linear(3, 2, 7), solve_linear(4, 2, 8), solve_linear(4, 3, 8))
    print(extended_gcd_table(26, 7), extended_gcd_table(240, 46))
    print(extended_gcd_iterative(26, 7), extended_gcd_iterative(240, 46), smallest_positive_combination(84, 36))
    print(solve_congruence(4, 4, 8), solve_congruence(6, 4, 10), solve_congruence(4, 2, 8), solve_congruence(3, 2, 7))
    print(inverses_up_to(7), inverse_by_fermat(3, 7), inverse(2753, 3120), solve_congruence(15, 6, 21))
