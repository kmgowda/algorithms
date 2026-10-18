"""Volume 7, Chapter 10 - Bloom Filters and Probabilistic Structures.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import hashlib
import math


def hash_i(item: str, i: int, m: int) -> int:
    """The i-th hash of item, in range(m). Built from SHA-256 so results are the same on every run."""
    digest = hashlib.sha256(f"{i}:{item}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % m


class BloomFilter:
    """m bits, k hash functions. 'No' answers are always right; 'maybe' answers are wrong with a small,
    predictable probability. No deletions."""

    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        self.m = max(8, math.ceil(-expected_items * math.log(false_positive_rate) / math.log(2) ** 2))
        self.k = max(1, round(self.m / expected_items * math.log(2)))
        self.bits = bytearray((self.m + 7) // 8)

    def _positions(self, item: str) -> list[int]:
        return [hash_i(item, i, self.m) for i in range(self.k)]

    def add(self, item: str) -> None:
        for p in self._positions(item):
            self.bits[p // 8] |= 1 << (p % 8)

    def might_contain(self, item: str) -> bool:
        return all(self.bits[p // 8] >> (p % 8) & 1 for p in self._positions(item))


class CountMinSketch:
    """Approximate counts in fixed memory: d rows of w counters; an item adds 1 to one counter per row.
    The estimate is the smallest of its d counters - never too low, rarely much too high."""

    def __init__(self, width: int, depth: int) -> None:
        self.w, self.d = width, depth
        self.rows = [[0] * width for _ in range(depth)]

    def add(self, item: str, count: int = 1) -> None:
        for r in range(self.d):
            self.rows[r][hash_i(item, r, self.w)] += count

    def estimate(self, item: str) -> int:
        return min(self.rows[r][hash_i(item, r, self.w)] for r in range(self.d))


class HyperLogLog:
    """Approximate COUNT DISTINCT in a few kilobytes. Idea: in random bit strings, a run of z leading zeros
    suggests about 2^z distinct items were seen. 2^p registers average out the luck."""

    def __init__(self, p: int = 10) -> None:
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m

    def add(self, item: str) -> None:
        x = int.from_bytes(hashlib.sha256(item.encode()).digest()[:8], "big")      # 64 random-looking bits
        bucket = x >> (64 - self.p)                                                   # first p bits pick a register
        rest = (x << self.p) & ((1 << 64) - 1)
        rank = 64 - self.p + 1 if rest == 0 else (64 - rest.bit_length()) + 1         # leading zeros + 1
        self.registers[bucket] = max(self.registers[bucket], rank)

    def count(self) -> float:
        alpha = 0.7213 / (1 + 1.079 / self.m)
        raw = alpha * self.m * self.m / sum(2.0 ** -r for r in self.registers)
        zeros = self.registers.count(0)
        if raw <= 2.5 * self.m and zeros:                                             # small-range correction
            return self.m * math.log(self.m / zeros)
        return raw


def crawler_skip_seen(urls: list[str]) -> int:
    """Industry example: a web crawler skips URLs it has (probably) visited, using a Bloom filter."""
    seen, fetched = BloomFilter(expected_items=len(urls), false_positive_rate=0.01), 0
    for u in urls:
        if not seen.might_contain(u):
            fetched += 1
            seen.add(u)
    return fetched


if __name__ == "__main__":
    bf = BloomFilter(1000, 0.01)
    for i in range(1000):
        bf.add(f"user{i}@mail.com")
    false_pos = sum(bf.might_contain(f"stranger{i}@mail.com") for i in range(10_000))
    print(f"bloom: {bf.m} bits ({bf.m // 8} bytes), k={bf.k}, false positives {false_pos}/10000")
    cms = CountMinSketch(width=200, depth=4)
    for word, times in [("lion", 500), ("zebra", 120), ("okapi", 3)]:
        cms.add(word, times)
    for i in range(2000):
        cms.add(f"noise{i}")
    print("count-min estimates:", {w: cms.estimate(w) for w in ("lion", "zebra", "okapi")})
    hll = HyperLogLog(p=10)
    for i in range(50_000):
        hll.add(f"visitor-{i % 20_000}")
    print("HyperLogLog distinct visitors ~", round(hll.count()), "(true 20000)")
    print("crawler fetched:", crawler_skip_seen([f"page{i % 300}" for i in range(1000)]), "of 300 distinct pages")
