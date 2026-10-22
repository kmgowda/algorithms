"""Volume 7, Chapter 6 - Testing Primes Quickly: Fermat's test, its liars, and Miller-Rabin.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import random

BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]      # exact for every n below EXACT_BELOW (about 3.19 * 10^23)
EXACT_BELOW = 318_665_857_834_031_151_167_461                # Sorenson and Webster (2015); adding base 41 reaches 3.3 * 10^24


def fermat(n: int, a: int) -> bool:
    """Passes if a^(n-1) mod n = 1, as every prime does (Figure 6.1)."""
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


def verdict(n: int) -> str:
    """'composite' (certain), 'prime' (certain: below the proven limit of the fixed bases), or 'probably prime'."""
    if not miller_rabin(n):
        return "composite"
    return "prime" if n < EXACT_BELOW else "probably prime"


def squaring_chain(n: int, a: int) -> list:
    """a^d, a^(2d), ..., a^(2^s d) mod n for n - 1 = 2^s * d (Figure 6.3)."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x, out = pow(a, d, n), []
    out.append(x)
    for _ in range(s):
        x = x * x % n
        out.append(x)
    return out


def is_strong_liar(n: int, a: int) -> bool:
    """True when base a fails to expose the odd number n (n passes the Miller-Rabin round for a)."""
    chain = squaring_chain(n, a)
    return chain[0] == 1 or (n - 1) in chain[:-1]


def liar_counts(n: int) -> tuple[int, int, int]:
    """(Fermat liars, strong liars, bases tried) among 1..n-1 for an odd composite n."""
    fermat_liars = sum(1 for a in range(1, n) if pow(a, n - 1, n) == 1)
    strong = sum(1 for a in range(1, n) if is_strong_liar(n, a))
    return fermat_liars, strong, n - 1


def worst_strong_liar_share(limit: int) -> tuple[float, int]:
    """The largest share of strong liars over odd composites below limit (Rabin: never above 1/4)."""
    best = (0.0, 0)
    for n in range(9, limit, 2):
        if trial(n):
            continue
        share = liar_counts(n)[1] / (n - 1)
        best = max(best, (share, n))
    return best


def korselt(n: int) -> bool:
    """Korselt's criterion for a Carmichael number: composite, square-free, and p - 1 divides n - 1 for every prime p | n."""
    if n < 3 or trial(n):
        return False
    m, p = n, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0 or (n - 1) % (p - 1):
                return False
        p += 1
    if m > 1 and (n - 1) % (m - 1):
        return False
    return True


def pollard_rho(n: int, c: int = 1, log: list | None = None) -> int | None:
    """Pollard's rho with Floyd's tortoise and hare: x -> x^2 + c mod n. Returns a factor of n (maybe n itself, if
    unlucky: retry with another c), or None for n < 2. log collects (step, tortoise, hare, gcd)."""
    import math
    if n < 2:
        return None
    if n % 2 == 0:
        return 2
    x = y = 2
    d, step = 1, 0
    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(abs(x - y), n)
        step += 1
        if log is not None:
            log.append((step, x, y, d))
    return d


def factor_completely(n: int) -> list:
    """Every prime factor of n, using Miller-Rabin to recognise primes and Pollard's rho to split composites."""
    if n < 2:
        return []
    if miller_rabin(n):
        return [n]
    for p in BASES:
        if n % p == 0:
            return sorted([p] + factor_completely(n // p))
    c = 1
    while True:
        d = pollard_rho(n, c)
        if d not in (None, n):
            return sorted(factor_completely(d) + factor_completely(n // d))
        c += 1


def filter_share(limit: int) -> float:
    """Share of odd numbers removed by dividing by the odd primes below limit (the cheap filter before Miller-Rabin)."""
    share_left = 1.0
    for p in range(3, limit):
        if trial(p):
            share_left *= 1 - 1 / p
    return 1 - share_left


def next_prime(n: int) -> int:
    while not miller_rabin(n):
        n += 1
    return n


if __name__ == "__main__":
    print(fermat(97, 2), fermat(91, 2), fermat(341, 2), 341 == 11 * 31, fermat(561, 2), fermat(561, 5), miller_rabin(341), miller_rabin(561))
    carmichael = [n for n in range(3, 10000, 2) if not trial(n) and all(fermat(n, a) for a in range(2, n) if __import__("math").gcd(a, n) == 1)]
    print(carmichael)
    p = next_prime(10 ** 30)
    print(p, miller_rabin(2 ** 61 - 1), miller_rabin(2 ** 61 + 1), verdict(2 ** 61 - 1), verdict(p), verdict(561))
    print(squaring_chain(561, 2), squaring_chain(341, 2), squaring_chain(97, 2), squaring_chain(561, 5))
    print(liar_counts(561), liar_counts(341), liar_counts(9), worst_strong_liar_share(3000))
    print([n for n in range(3, 10000) if korselt(n)])
    log = []
    print(pollard_rho(8051, 1, log), log, factor_completely(2 ** 64 + 1), factor_completely(10 ** 18 + 9))
