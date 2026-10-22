"""Volume 7, Chapter 4 - Thinking Problems (Section 4.16): model solutions.

Run:  python3 ch04_solutions.py
"""

from __future__ import annotations

import math

from ch04_examples import solve_congruence


def affine_keys(n1: int, c1: int, n2: int, c2: int, m: int = 26) -> list:
    """Thinking Problem 2: every key (k, s) of the cipher c = k*n + s (mod m), with gcd(k, m) = 1,
    that sends letter n1 to c1 and letter n2 to c2.

    Subtracting the two equations leaves k*(n1 - n2) = c1 - c2 (mod m), a linear congruence; each of its
    solutions k that is coprime to m gives one key, with s = c1 - k*n1 mod m.
    """
    found = solve_congruence(n1 - n2, c1 - c2, m)
    if found is None:
        return []
    x0, step, count = found
    keys = []
    for j in range(count):
        k = x0 + j * step
        if math.gcd(k, m) == 1:
            keys.append((k, (c1 - k * n1) % m))
    return keys


def inverse_by_fermat_anyway(a: int, m: int) -> int:
    """Thinking Problem 3: the WRONG inverse a^(m - 2) mod m, used for a composite m."""
    return pow(a, m - 2, m)


def wilson_holds(n: int) -> bool:
    """Thinking Problem 1: does (n - 1)! leave remainder n - 1 when divided by n?"""
    return math.factorial(n - 1) % n == n - 1


if __name__ == "__main__":
    print(affine_keys(2, 17, 4, 5), affine_keys(0, 3, 13, 16))
    print(inverse_by_fermat_anyway(7, 26), [n for n in range(2, 40) if wilson_holds(n)])
