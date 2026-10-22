"""Volume 7, Chapter 8 - Thinking Problems (Section 8.17): model solutions.

Run:  python3 ch08_solutions.py
"""

from __future__ import annotations

import math


def common_modulus(c1: int, c2: int, e1: int, e2: int, n: int) -> int:
    """Thinking Problem 2: read m from c1 = m^e1 and c2 = m^e2 (mod n) when gcd(e1, e2) = 1, without a private key.

    Extended Euclid gives s*e1 + t*e2 = 1, so c1^s * c2^t = m^(s*e1 + t*e2) = m. A negative power needs an
    inverse; if a code shares a factor with n, that factor splits n, and the private key follows.
    """
    if math.gcd(e1, e2) != 1:
        raise ValueError("the two exponents must be coprime")
    for c, e in ((c1, e1), (c2, e2)):
        g = math.gcd(c, n)
        if g == n:
            return 0
        if g > 1:                                   # the message is a multiple of a secret prime
            p, q = g, n // g
            return pow(c, pow(e, -1, (p - 1) * (q - 1)), n)
    s, t = _bezout(e1, e2)
    return pow(c1, s, n) * pow(c2, t, n) % n          # pow with a negative power uses the inverse


def _bezout(a: int, b: int) -> tuple[int, int]:
    if b == 0:
        return 1, 0
    x, y = _bezout(b, a % b)
    return y, x - (a // b) * y


def euler_shortcut_check(m: int, n: int, phi: int) -> bool:
    """Thinking Problem 3: is m^phi(n) = 1 (mod n), the step the flawed argument relies on?"""
    return pow(m, phi, n) == 1


if __name__ == "__main__":
    n = 3233
    print(common_modulus(pow(65, 17, n), pow(65, 7, n), 17, 7, n), common_modulus(pow(61, 17, n), pow(61, 7, n), 17, 7, n))
    print(euler_shortcut_check(61, 3233, 3120), pow(61, 3120, 3233), pow(pow(7, 5, 49), 17, 49))
