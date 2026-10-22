"""Volume 7, Chapter 17 - Random Numbers and Fair Shuffles: a seeded generator, and Fisher-Yates.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

import random
from collections import Counter


class LCG:
    """A tiny linear congruential generator: x <- (a x + c) mod m (Figure 17.1). Fine for games, not for secrets."""

    def __init__(self, seed: int, a: int = 1103515245, c: int = 12345, m: int = 2 ** 31):
        self.x, self.a, self.c, self.m = seed, a, c, m

    def next(self) -> int:
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def below(self, n: int) -> int:
        return self.next() % n


def fisher_yates(items: list, rng) -> list:
    """Fair shuffle (Figure 17.2): swap each position with a random position at or before it."""
    a = list(items)
    for i in range(len(a) - 1, 0, -1):
        j = rng.randrange(i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def naive_shuffle(items: list, rng) -> list:
    """Swap each position with ANY position: looks fine, is biased."""
    a = list(items)
    for i in range(len(a)):
        j = rng.randrange(len(a))
        a[i], a[j] = a[j], a[i]
    return a


class ChoiceFeeder:
    """Feeds a fixed list of choices to a shuffle, to enumerate every possible run (Figure 17.3)."""

    def __init__(self, choices):
        self.choices = iter(choices)

    def randrange(self, n):
        return next(self.choices)


def all_fisher_yates_runs(n: int) -> Counter:
    """Every possible run of Fisher-Yates on n items (choices j_i in 0..i for i = n-1 down to 1): n! runs."""
    import itertools
    ranges = [range(i + 1) for i in range(n - 1, 0, -1)]
    return Counter(tuple(fisher_yates(list(range(n)), ChoiceFeeder(c))) for c in itertools.product(*ranges))


def all_naive_runs(n: int) -> Counter:
    import itertools
    return Counter(tuple(naive_shuffle(list(range(n)), ChoiceFeeder(c))) for c in itertools.product(range(n), repeat=n))


def full_period(a: int, c: int, m: int) -> bool:
    """Hull-Dobell: x <- (a x + c) mod m visits all m values exactly when gcd(c, m) = 1, a - 1 is divisible by every
    prime factor of m, and by 4 if m is."""
    import math
    if math.gcd(c, m) != 1:
        return False
    n, p = m, 2
    while p * p <= n:
        if n % p == 0:
            if (a - 1) % p:
                return False
            while n % p == 0:
                n //= p
        p += 1
    if n > 1 and (a - 1) % n:
        return False
    return not (m % 4 == 0 and (a - 1) % 4)


def period(a: int, c: int, m: int, seed: int) -> int:
    x, seen, k = seed, {}, 0
    while x not in seen:
        seen[x] = k
        x = (a * x + c) % m
        k += 1
    return k - seen[x]


def modulo_bias(source: int, n: int) -> list:
    """How often each of 0..n-1 appears when every value 0..source-1 is reduced with % n."""
    counts = [0] * n
    for v in range(source):
        counts[v % n] += 1
    return counts


def below_by_rejection(rng_byte, n: int) -> tuple[int, int]:
    """A fair number in 0..n-1 from fair bytes 0..255: reject bytes at or above the largest multiple of n (Figure 17.4).
    Returns (number, bytes used)."""
    limit, used = 256 - 256 % n, 0
    while True:
        b = rng_byte()
        used += 1
        if b < limit:
            return b % n, used


def partial_shuffle(items: list, k: int, rng) -> list:
    """The last k positions after k steps of Fisher-Yates: a uniformly random ordered sample of k items."""
    a = list(items)
    for i in range(len(a) - 1, len(a) - 1 - k, -1):
        j = rng.randrange(i + 1)
        a[i], a[j] = a[j], a[i]
    return a[len(a) - k:] if k else []


def count_orders(shuffle, trials: int, seed: int) -> Counter:
    rng = random.Random(seed)
    return Counter("".join(shuffle(list("abc"), rng)) for _ in range(trials))


if __name__ == "__main__":
    g = LCG(42)
    print([g.below(100) for _ in range(8)], [LCG(42).below(100) for _ in range(2)])
    print(sorted(count_orders(fisher_yates, 60000, 17).items()))
    print(sorted(count_orders(naive_shuffle, 60000, 17).items()))
    print(sorted(all_fisher_yates_runs(4).values()) == [1] * 24, sorted(set(all_naive_runs(4).values())), 4 ** 4, sorted(all_naive_runs(3).items()))
    print(full_period(5, 3, 8), period(5, 3, 8, 5), full_period(1103515245, 12345, 2 ** 31), full_period(4, 3, 8), period(4, 3, 8, 5), full_period(5, 2, 8))
    print(modulo_bias(256, 10), modulo_bias(256, 3))
    r = random.Random(7)
    print(below_by_rejection(lambda: r.randrange(256), 10), partial_shuffle(list(range(10)), 3, random.Random(3)))
    import math
    print([n for n in range(2, 10) if n ** n % math.factorial(n) == 0])
