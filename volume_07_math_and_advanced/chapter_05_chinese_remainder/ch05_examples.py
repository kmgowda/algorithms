"""Volume 7, Chapter 5 - The Chinese Remainder Theorem: one number from its remainders.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import math


def crt(remainders: list, moduli: list) -> tuple[int | None, int]:
    """The smallest x >= 0 with x mod m_i = r_i for every i, and the combined modulus (Figure 5.2).
    Moduli need not be coprime; returns (None, lcm) when the remainders contradict each other."""
    x, m = 0, 1
    for r, n in zip(remainders, moduli):
        if n <= 0:
            raise ValueError("moduli must be positive")
        g = math.gcd(m, n)
        if (r - x) % g:
            return None, m * n // g
        k = ((r - x) // g) * pow(m // g, -1, n // g) % (n // g)
        x += m * k
        m = m * n // g
        x %= m
    return x, m


def crt_by_search(remainders: list, moduli: list) -> int | None:
    m = math.lcm(*moduli) if moduli else 1
    return next((x for x in range(m) if all(x % n == r % n for r, n in zip(remainders, moduli))), None)


def crt_formula(remainders: list, moduli: list) -> tuple[int, int, list]:
    """The explicit formula for pairwise coprime moduli: x = sum of r_i * M_i * y_i mod M, with M_i = M / m_i and
    y_i the inverse of M_i mod m_i (Figure 5.3). Returns (x, M, terms) where terms are (M_i, y_i, r_i * M_i * y_i)."""
    M = math.prod(moduli)
    terms = []
    for r, n in zip(remainders, moduli):
        if n <= 0:
            raise ValueError("moduli must be positive")
        Mi = M // n
        yi = pow(Mi, -1, n) if n > 1 else 0
        terms.append((Mi, yi, r * Mi * yi))
    return sum(t[2] for t in terms) % M, M, terms


def crt_trace(remainders: list, moduli: list) -> list:
    """Incremental combining with its trace: after each condition, (k, x, combined modulus)."""
    x, m, out = 0, 1, []
    for r, n in zip(remainders, moduli):
        g = math.gcd(m, n)
        if (r - x) % g:
            out.append((None, None, m * n // g))
            return out
        k = ((r - x) // g) * pow(m // g, -1, n // g) % (n // g)
        x, m = (x + m * k) % (m * n // g), m * n // g
        out.append((k, x, m))
    return out


RNS = [97, 98, 99]


def to_residues(n: int, moduli: list = RNS) -> list:
    return [n % m for m in moduli]


def residue_add(a: list, b: list, moduli: list = RNS) -> list:
    return [(x + y) % m for x, y, m in zip(a, b, moduli)]


def residue_mul(a: list, b: list, moduli: list = RNS) -> list:
    return [x * y % m for x, y, m in zip(a, b, moduli)]


def from_residues(res: list, moduli: list = RNS) -> int:
    return crt(res, moduli)[0]


if __name__ == "__main__":
    print(crt([2, 3, 2], [3, 5, 7]), crt_by_search([2, 3, 2], [3, 5, 7]))
    print(crt([1, 2, 3, 4], [2, 3, 5, 7]), crt([3, 4], [6, 8]), crt([1, 2], [4, 6]), crt([2, 4], [6, 8]))
    print(crt_formula([2, 3, 2], [3, 5, 7]), crt_trace([2, 3, 2], [3, 5, 7]), crt_trace([2, 4], [6, 8]))
    a, b = to_residues(500_000), to_residues(400_000)
    print(a, b, from_residues(residue_add(a, b)), from_residues(residue_mul(to_residues(700), to_residues(1300))), math.prod(RNS))
