"""Volume 2, Chapter 32 - Bloom Filters.

Run:  python3 ch32_examples.py
"""

from __future__ import annotations

import hashlib
import math


class BloomFilter:
    """m bits and k hash functions: 'definitely not present' or 'probably present' (Figure 32.1)."""

    def __init__(self, m: int, k: int):
        if m < 1 or k < 1:                            # with k = 0, every item would "probably" be present
            raise ValueError("need at least one bit and one hash function")
        self.m, self.k = m, k
        self.bits = bytearray(m)

    def positions(self, item: str) -> list[int]:
        """k bit positions for an item, from two halves of one strong hash (double hashing)."""
        d = hashlib.sha256(item.encode()).digest()
        h1 = int.from_bytes(d[:8], "big")
        h2 = int.from_bytes(d[8:16], "big") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item: str) -> None:
        for p in self.positions(item):
            self.bits[p] = 1

    def might_contain(self, item: str) -> bool:
        return all(self.bits[p] for p in self.positions(item))


def false_positive_rate(m: int, n: int, k: int) -> float:
    """The classic estimate (1 - e^(-kn/m))^k."""
    return (1 - math.exp(-k * n / m)) ** k


def best_k(m: int, n: int) -> int:
    return max(1, round(m / n * math.log(2)))


def measure(m: int, n: int, k: int, trials: int = 20_000) -> float:
    bf = BloomFilter(m, k)
    for i in range(n):
        bf.add(f"book-{i}")
    return sum(bf.might_contain(f"other-{j}") for j in range(trials)) / trials


def screen(owned: int = 200_000, proposals: int = 5_000, already: int = 500, bits_per: int = 10):
    """Section 32.8: returns (false negatives, false positives among new titles, new titles)."""
    m = owned * bits_per
    bf = BloomFilter(m, best_k(m, owned))
    for i in range(owned):
        bf.add(f"title-{i}")
    owned_hits = sum(not bf.might_contain(f"title-{i}") for i in range(already))
    new = proposals - already
    false_yes = sum(bf.might_contain(f"new-{j}") for j in range(new))
    return owned_hits, false_yes, new


if __name__ == "__main__":
    print(screen())
    small = BloomFilter(16, 3)
    for t in ("Maps", "Ocean", "Clocks"):
        small.add(t)
        print(t, small.positions(t))
    print("Stars", small.positions("Stars"), small.might_contain("Stars"))
    n = 10_000
    for bits_per in (4, 8, 10, 16):
        m = n * bits_per
        k = best_k(m, n)
        print(bits_per, k, round(false_positive_rate(m, n, k), 4), round(measure(m, n, k), 4))
