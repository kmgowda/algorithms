"""Volume 14, Chapter 3 - Number Theory I: Divisibility, GCD, Primes, Sieve.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import timeit


def divisors(n: int) -> list[int]:
    """All divisors of n in O(sqrt n): divisors come in pairs d and n // d, one of them <= sqrt n."""
    small, large = [], []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def gcd(a: int, b: int) -> int:
    """Euclid (V2-C9): gcd(a, b) = gcd(b, a mod b); the numbers shrink at least by half every two steps."""
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """Least common multiple: a x b = gcd x lcm."""
    return abs(a // gcd(a, b) * b) if a and b else 0


def is_prime(n: int) -> bool:
    """Trial division up to sqrt n, skipping even numbers."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def sieve(limit: int) -> list[int]:
    """Sieve of Eratosthenes: cross out multiples of each prime, starting at its square. O(n log log n)."""
    if limit < 2:
        return []
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    p = 2
    while p * p <= limit:
        if is_p[p]:
            is_p[p * p::p] = bytearray(len(range(p * p, limit + 1, p)))
        p += 1
    return [i for i in range(limit + 1) if is_p[i]]


def factorize(n: int) -> dict[int, int]:
    """Prime factorization by trial division: {prime: exponent}."""
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def race(limit: int) -> dict[str, float]:
    return {"trial division each": min(timeit.repeat(lambda: [n for n in range(limit) if is_prime(n)], number=1, repeat=3)),
            "sieve": min(timeit.repeat(lambda: sieve(limit - 1), number=1, repeat=3))}


def bus_meeting_time(intervals: list[int]) -> int:
    """Industry example: buses leave the depot every 12, 18 and 30 minutes - when do all leave together again?"""
    out = 1
    for x in intervals:
        out = lcm(out, x)
    return out


if __name__ == "__main__":
    print(divisors(36), gcd(84, 36), lcm(4, 6), is_prime(97), sieve(30), factorize(360))
    print({k: f"{v * 1000:.1f} ms" for k, v in race(200000).items()})
    print("buses meet again after", bus_meeting_time([12, 18, 30]), "minutes")
