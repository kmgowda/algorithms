"""Volume 6, Chapter 6 - Testing Primes Quickly: Fermat's test, its liars, and Miller-Rabin.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import random

BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]      # enough to be exact for every n below 3.3 * 10^24


def fermat(n: int, a: int) -> bool:
    """Passes if a^(n-1) mod n = 1, as every prime does (Figure 6.2)."""
    return pow(a, n - 1, n) == 1


def miller_rabin(n: int, bases=BASES) -> bool:
    """Write n - 1 = 2^s * d; for each base, a^d must be 1, or reach n - 1 while squaring (Figure 6.3)."""
    if n < 2:
        return False
    for p in BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False                              # a is a witness: n is certainly composite
    return True


def trial(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def next_prime(n: int) -> int:
    while not miller_rabin(n):
        n += 1
    return n


if __name__ == "__main__":
    print(fermat(97, 2), fermat(91, 2), fermat(341, 2), 341 == 11 * 31, fermat(561, 2), fermat(561, 5), miller_rabin(341), miller_rabin(561))
    carmichael = [n for n in range(3, 10000, 2) if not trial(n) and all(fermat(n, a) for a in range(2, n) if __import__("math").gcd(a, n) == 1)]
    print(carmichael)
    p = next_prime(10 ** 30)
    print(p, miller_rabin(2 ** 61 - 1), miller_rabin(2 ** 61 + 1))
