"""Volume 6, Chapter 2 - Primes and the Sieve: test one number, or find every prime up to a limit.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import time


def is_prime(n: int) -> tuple[bool, int]:
    """Trial division up to the square root (Figure 2.2). Returns (prime?, divisions tried)."""
    if n < 2:
        return False, 0
    tries, d = 0, 2
    while d * d <= n:
        tries += 1
        if n % d == 0:
            return False, tries
        d += 1
    return True, tries


def sieve(limit: int) -> tuple[list, int]:
    """Sieve of Eratosthenes (Figure 2.3): cross out multiples of each prime from its square.
    Returns (primes up to limit, crossings-out made)."""
    if limit < 2:
        return [], 0
    alive = [True] * (limit + 1)
    alive[0] = alive[1] = False
    crossings, p = 0, 2
    while p * p <= limit:
        if alive[p]:
            for m in range(p * p, limit + 1, p):
                crossings += 1
                alive[m] = False
        p += 1
    return [i for i, a in enumerate(alive) if a], crossings


def factorise(n: int) -> list:
    """Prime factors of n, smallest first, by trial division."""
    if n < 1:
        raise ValueError("factorise needs a positive whole number")
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


if __name__ == "__main__":
    print(sieve(50))
    print(is_prime(97), is_prime(91), is_prime(1_000_003), factorise(84), factorise(720720))
    for lim in (100, 10_000, 1_000_000):
        t = time.perf_counter(); p, c = sieve(lim); print(lim, len(p), c, round((time.perf_counter() - t) * 1000))
