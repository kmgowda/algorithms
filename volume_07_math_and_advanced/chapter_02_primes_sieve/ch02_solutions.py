"""Volume 7, Chapter 2 - Thinking Problems (Section 2.15): model solutions.

Run:  python3 ch02_solutions.py
"""

from __future__ import annotations

import math


def distinct_prime_counts(limit: int) -> list:
    """Thinking Problem 2: omega[m] = the number of different primes dividing m, for 0 <= m <= limit.

    A sieve that never stops early: every prime p adds 1 to each of its multiples, about limit / p
    additions, so about limit * ln ln limit in all. omega[0] and omega[1] stay 0.
    """
    omega = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if omega[p] == 0:                       # untouched so far, so p is prime
            for m in range(p, limit + 1, p):
                omega[m] += 1
    return omega


def segmented_sieve_buggy(lo: int, hi: int) -> list:
    """Thinking Problem 3: the WRONG window sieve that starts at the first multiple >= lo, not at p * p."""
    lo = max(lo, 2)
    small = [p for p in range(2, math.isqrt(hi) + 1) if all(p % d for d in range(2, math.isqrt(p) + 1))]
    alive = [True] * (hi - lo + 1)
    for p in small:
        for m in range((lo + p - 1) // p * p, hi + 1, p):
            alive[m - lo] = False
    return [lo + i for i, a in enumerate(alive) if a]


def composite_run(n: int) -> list:
    """Thinking Problem 1: n consecutive composites, (n + 1)! + 2 .. (n + 1)! + (n + 1)."""
    f = math.factorial(n + 1)
    return [f + k for k in range(2, n + 2)]


if __name__ == "__main__":
    print(distinct_prime_counts(12), distinct_prime_counts(1))
    print(segmented_sieve_buggy(2, 20), composite_run(4))
