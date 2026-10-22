"""Volume 7, Chapter 2 - Primes and the Sieve: test one number, or find every prime up to a limit.

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


def factorise_steps(n: int) -> list:
    """Trial-division factorisation with its trace: (divisor tried, what is left after removing it)."""
    if n < 1:
        raise ValueError("factorise needs a positive whole number")
    trace, d = [], 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            trace.append((d, n))
        d += 1
    if n > 1:
        trace.append((n, 1))
    return trace


def smallest_factor_sieve(limit: int) -> tuple[list, int]:
    """Linear (Euler) sieve: spf[m] = the smallest prime factor of m for 2 <= m <= limit (Figure 2.4).
    Each composite is written exactly once, by its smallest prime factor. Returns (spf, writes)."""
    spf = [0] * (limit + 1)
    primes, writes = [], 0
    for i in range(2, limit + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > limit:
                break
            spf[i * p] = p
            writes += 1
    return spf, writes


def factorise_with_spf(n: int, spf: list) -> list:
    """Factorise n in at most log2(n) divisions by repeatedly dividing by its smallest prime factor."""
    if n < 1:
        raise ValueError("factorise needs a positive whole number")
    out = []
    while n > 1:
        out.append(spf[n])
        n //= spf[n]
    return out


def segmented_sieve(lo: int, hi: int) -> list:
    """Primes in lo..hi (inclusive) using only the primes up to sqrt(hi) and a window of hi - lo + 1 marks."""
    if hi < 2 or hi < lo:
        return []
    lo = max(lo, 2)
    small, _ = sieve(int(hi ** 0.5) + 1)
    alive = [True] * (hi - lo + 1)
    for p in small:
        start = max(p * p, (lo + p - 1) // p * p)
        for m in range(start, hi + 1, p):
            alive[m - lo] = False
    return [lo + i for i, a in enumerate(alive) if a]


def reciprocal_prime_sum(x: int) -> float:
    """Sum of 1/p over primes p <= x; Mertens: about ln ln x + 0.2615."""
    return sum(1 / p for p in sieve(x)[0])


if __name__ == "__main__":
    print(sieve(50))
    print(is_prime(97), is_prime(91), is_prime(1_000_003), factorise(84), factorise(720720))
    for lim in (100, 10_000, 1_000_000):
        t = time.perf_counter(); p, c = sieve(lim); print(lim, len(p), c, round((time.perf_counter() - t) * 1000))
    import math
    for lim in (100, 10_000, 1_000_000, 10_000_000):
        p, c = sieve(lim)
        print("per number", lim, round(c / lim, 3), round(math.log(math.log(lim)), 3), "pnt", round(lim / math.log(lim)), len(p))
    print(factorise_steps(360), factorise_steps(97), factorise_steps(1_000_003 * 2))
    spf, w = smallest_factor_sieve(1_000_000)
    print(spf[2:31], w, 1_000_000 - 78498 - 1, factorise_with_spf(360, spf), factorise_with_spf(720720, spf))
    print(round(reciprocal_prime_sum(1000), 4), round(math.log(math.log(1000)) + 0.2615, 4))
    seg = segmented_sieve(10 ** 12, 10 ** 12 + 1000)
    print(len(seg), seg[:3])
