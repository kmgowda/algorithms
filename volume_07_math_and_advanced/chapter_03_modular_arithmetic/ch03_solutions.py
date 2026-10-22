"""Volume 7, Chapter 3 - Thinking Problems (Section 3.15): model solutions.

Run:  python3 ch03_solutions.py
"""

from __future__ import annotations

from ch03_examples import power_mod


def tower_mod(a: int, b: int, c: int, p: int) -> int:
    """Thinking Problem 2: a^(b^c) mod a prime p, without ever writing down b^c.

    If p divides a, the answer is 0 unless the exponent b^c is 0 (b = 0 and c > 0), when it is 1 mod p.
    Otherwise Fermat lets the exponent shrink mod p - 1, and b^c mod (p - 1) is itself a fast power.
    """
    if a % p == 0:
        return 1 % p if b == 0 and c > 0 else 0
    e, _ = power_mod(b, c, p - 1)
    return power_mod(a, e, p)[0]


def power_reduced_exponent(a: int, e: int, n: int, phi_n: int) -> int:
    """Thinking Problem 3: the WRONG shortcut a^e mod n = a^(e mod phi(n)) mod n, used even when gcd(a, n) > 1."""
    return power_mod(a, e % phi_n, n)[0]


if __name__ == "__main__":
    print(tower_mod(10, 10, 100, 7), tower_mod(2, 3, 4, 13), pow(2, 3 ** 4, 13))
    print(power_reduced_exponent(2, 4, 12, 4), pow(2, 4, 12))
