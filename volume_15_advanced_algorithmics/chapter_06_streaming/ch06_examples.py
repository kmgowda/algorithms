"""Volume 15, Chapter 6 - Streaming Algorithms: Counting Distinct Items in Endless Data.

A streaming algorithm reads each item once, in order, using memory far smaller than the stream.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import hashlib
import math
import random
from typing import Hashable, Iterable


def majority_vote(stream: Iterable[Hashable]) -> Hashable | None:
    """Boyer-Moore majority vote (LeetCode 169): one candidate and one counter. If some item appears in more than
    half the stream, it is the survivor."""
    candidate, count = None, 0
    for x in stream:
        if count == 0:
            candidate, count = x, 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    return candidate


def misra_gries(stream: Iterable[Hashable], k: int) -> dict[Hashable, int]:
    """Heavy hitters with k - 1 counters: every item appearing more than n / k times survives. Each count is an
    UNDER-estimate by at most n / k."""
    counters: dict[Hashable, int] = {}
    for x in stream:
        if x in counters:
            counters[x] += 1
        elif len(counters) < k - 1:
            counters[x] = 1
        else:
            for key in list(counters):
                counters[key] -= 1
                if counters[key] == 0:
                    del counters[key]
    return counters


def _hash(x: Hashable, seed: int) -> int:
    return int.from_bytes(hashlib.blake2b(f"{seed}:{x}".encode(), digest_size=8).digest(), "big")


def hyperloglog(stream: Iterable[Hashable], b: int = 10) -> float:
    """Distinct count with 2^b small registers. Each item's hash picks a register (first b bits) and records the
    position of the first 1-bit in the rest: seeing a long run of leading zeros means many distinct items.
    Typical error about 1.04 / sqrt(2^b) - roughly 3% with 1,024 registers."""
    m = 1 << b
    registers = [0] * m
    for x in stream:
        h = _hash(x, 0)
        idx = h >> (64 - b)
        rest = (h << b) & ((1 << 64) - 1)
        rank = min(64 - rest.bit_length() + 1, 64 - b + 1)     # leading zeros + 1
        registers[idx] = max(registers[idx], rank)
    alpha = 0.7213 / (1 + 1.079 / m)
    estimate = alpha * m * m / sum(2.0 ** -r for r in registers)
    zeros = registers.count(0)
    if estimate <= 2.5 * m and zeros:
        estimate = m * math.log(m / zeros)                # small-range correction (linear counting)
    return estimate


class CountMin:
    """Count-min sketch (V7-C10): approximate frequencies in fixed memory; never under-counts."""

    def __init__(self, width: int, depth: int) -> None:
        self.width, self.depth = width, depth
        self.table = [[0] * width for _ in range(depth)]

    def add(self, x: Hashable) -> None:
        for row in range(self.depth):
            self.table[row][_hash(x, row + 1) % self.width] += 1

    def estimate(self, x: Hashable) -> int:
        return min(self.table[row][_hash(x, row + 1) % self.width] for row in range(self.depth))


def unique_visitors(page_views: Iterable[str]) -> tuple[int, int]:
    """Industry example: estimate unique visitors from a click stream with about 1 KB of registers."""
    exact, views = set(), []
    for v in page_views:
        exact.add(v)
        views.append(v)
    return round(hyperloglog(views, b=10)), len(exact)


if __name__ == "__main__":
    rng = random.Random(1)
    votes = ["A"] * 6 + ["B"] * 3 + ["C"] * 2
    rng.shuffle(votes)
    print("majority:", majority_vote(votes))
    words = [rng.choice(["the"] * 30 + ["data"] * 15 + ["stream"] * 10 + [f"w{i}" for i in range(200)]) for _ in range(20000)]
    top = sorted(misra_gries(words, 20).items(), key=lambda kv: -kv[1])[:3]
    print("heavy hitters (k=20):", top, "| true:", [(w, words.count(w)) for w, _ in top])
    for n in (1000, 100000):
        est = hyperloglog(range(n))
        print(f"distinct {n}: estimate {est:.0f}, error {abs(est - n) / n:.1%}")
    cm = CountMin(500, 4)
    for w in words:
        cm.add(w)
    print("count-min 'the':", cm.estimate("the"), "true", words.count("the"))
    clicks = [f"user{rng.randint(1, 30000)}" for _ in range(100000)]
    print("unique visitors (estimate, exact):", unique_visitors(clicks))
