"""Volume 6, Chapter 17 - Random Numbers and Fair Shuffles: a seeded generator, and Fisher-Yates.

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


def count_orders(shuffle, trials: int, seed: int) -> Counter:
    rng = random.Random(seed)
    return Counter("".join(shuffle(list("abc"), rng)) for _ in range(trials))


if __name__ == "__main__":
    g = LCG(42)
    print([g.below(100) for _ in range(8)], [LCG(42).below(100) for _ in range(2)])
    print(sorted(count_orders(fisher_yates, 60000, 17).items()))
    print(sorted(count_orders(naive_shuffle, 60000, 17).items()))
