"""Volume 7, Chapter 5 - Thinking Problems (Section 5.15): model solutions.

Run:  python3 ch05_solutions.py
"""

from __future__ import annotations

import math


def mixed_radix_digits(remainders: list, moduli: list) -> list:
    """Garner's digits d_i with x = d_1 + d_2*m_1 + d_3*m_1*m_2 + ..., 0 <= d_i < m_i (pairwise coprime moduli).
    Every calculation is modulo one m_i, so no number near the product M is ever formed."""
    digits = []
    for i, (r, n) in enumerate(zip(remainders, moduli)):
        v = r % n
        for j in range(i):
            v = (v - digits[j]) * pow(moduli[j] % n, -1, n) % n if n > 1 else 0
        digits.append(v)
    return digits


def rebuilt_mod(remainders: list, moduli: list, q: int) -> int:
    """Thinking Problem 2: (the number with these remainders) mod q, computed from Garner's digits
    with arithmetic modulo q only."""
    ans, weight = 0, 1 % q
    for d, n in zip(mixed_radix_digits(remainders, moduli), moduli):
        ans = (ans + d * weight) % q
        weight = weight * n % q
    return ans


def square_roots_of_one(n: int) -> list:
    """Thinking Problem 1: every x in 0..n-1 with x*x mod n = 1 mod n."""
    return [x for x in range(n) if x * x % n == 1 % n]


def unique_if_setwise_coprime(moduli: list) -> bool:
    """Thinking Problem 3: the WRONG test 'gcd of all the moduli is 1' for a unique answer below the product."""
    return math.gcd(*moduli) == 1


if __name__ == "__main__":
    print(mixed_radix_digits([2, 3, 2], [3, 5, 7]), rebuilt_mod([2, 3, 2], [3, 5, 7], 4), 23 % 4)
    print(square_roots_of_one(15), square_roots_of_one(105), unique_if_setwise_coprime([6, 10, 15]))
