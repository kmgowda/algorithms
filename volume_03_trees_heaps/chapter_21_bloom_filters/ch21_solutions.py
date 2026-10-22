"""Volume 3, Chapter 21 - Bloom Filters: companion code for the Thinking Problems (Section 21.16).

Run:  python3 ch21_solutions.py
"""

from __future__ import annotations

import hashlib
import math

from ch21_examples import BloomFilter


def fold(bf: BloomFilter) -> BloomFilter:
    """Thinking Problem 1: OR the two halves of a filter with an even number of bits."""
    half = BloomFilter(bf.m // 2, bf.k)
    for i in range(half.m):
        half.bits[i] = bf.bits[i] | bf.bits[i + half.m]
    return half


class CountingOnesFilter(BloomFilter):
    """Thinking Problem 2: a Bloom filter that keeps count of its 1 bits, to estimate how many items it holds."""

    def __init__(self, m: int, k: int):
        super().__init__(m, k)
        self.ones = 0

    def add(self, item: str) -> None:
        for p in self.positions(item):
            if not self.bits[p]:
                self.bits[p] = 1
                self.ones += 1

    def estimate(self) -> float:
        """About how many distinct items were added: -(m/k) ln(1 - ones/m). O(1)."""
        if self.ones == self.m:
            return math.inf                  # a full filter could hold any number of items
        return -self.m / self.k * math.log(1 - self.ones / self.m)


class NeighbourBitsFilter(BloomFilter):
    """Thinking Problem 3, the bug: k 'hash functions' that are one hash plus 0, 1, ..., k - 1."""

    def positions(self, item: str) -> list[int]:
        h = int.from_bytes(hashlib.sha256(item.encode()).digest()[:8], "big")
        return [(h + i) % self.m for i in range(self.k)]


def compare_rates(m: int = 10_000, n: int = 1_000, k: int = 7, trials: int = 100_000) -> tuple[float, float]:
    """Thinking Problem 3: measured false-positive rates of the real filter and the neighbour-bits filter."""
    out = []
    for cls in (BloomFilter, NeighbourBitsFilter):
        bf = cls(m, k)
        for i in range(n):
            bf.add(f"book-{i}")
        out.append(sum(bf.might_contain(f"other-{j}") for j in range(trials)) / trials)
    return out[0], out[1]


if __name__ == "__main__":
    f = CountingOnesFilter(10_000, 7)
    for i in range(1_000):
        f.add(f"book-{i}")
    print(f.ones, round(f.estimate(), 1))
    print(compare_rates())
