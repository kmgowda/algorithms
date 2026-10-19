"""Volume 14, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from ch03_examples import factorize, gcd, sieve


def count_primes(n: int) -> int:
    """Exercise 1 (LeetCode 204): primes strictly less than n."""
    return len(sieve(n - 1))


def gcd_of_strings(a: str, b: str) -> str:
    """Exercise 2 (LeetCode 1071): the longest string that divides both - exists only if a + b == b + a,
    and then its length is gcd(len(a), len(b))."""
    return a[:gcd(len(a), len(b))] if a + b == b + a else ""


def count_divisors(n: int) -> int:
    """Exercise 3: from n = p1^e1 x p2^e2 ..., the number of divisors is (e1 + 1)(e2 + 1)..."""
    out = 1
    for e in factorize(n).values():
        out *= e + 1
    return out


def ugly_number(n: int) -> bool:
    """Exercise 4 (LeetCode 263): only prime factors 2, 3 and 5."""
    return n > 0 and set(factorize(n)) <= {2, 3, 5}


if __name__ == "__main__":
    print(count_primes(10), gcd_of_strings("ABCABC", "ABC"), count_divisors(360), ugly_number(30), ugly_number(14))
