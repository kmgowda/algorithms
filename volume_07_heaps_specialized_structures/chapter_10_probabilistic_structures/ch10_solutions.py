"""Volume 7, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch10_examples import BloomFilter, CountMinSketch


def bloom_size(n: int, p: float) -> tuple[int, int]:
    """Exercise 1: bits m = -n ln p / (ln 2)^2 and hashes k = (m / n) ln 2."""
    m = math.ceil(-n * math.log(p) / math.log(2) ** 2)
    return m, max(1, round(m / n * math.log(2)))


def predicted_false_positive(m: int, k: int, n: int) -> float:
    """Exercise 2: probability all k bits are already set: (1 - e^(-k n / m))^k."""
    return (1 - math.exp(-k * n / m)) ** k


def measured_false_positive(n: int, p: float, trials: int = 20_000) -> float:
    bf = BloomFilter(n, p)
    for i in range(n):
        bf.add(f"in-{i}")
    return sum(bf.might_contain(f"out-{i}") for i in range(trials)) / trials


def heavy_hitters(stream: list[str], threshold: int, width: int = 100, depth: int = 4) -> list[str]:
    """Exercise 3: items whose estimated count reaches threshold (may include a few false alarms)."""
    cms = CountMinSketch(width, depth)
    for x in stream:
        cms.add(x)
    return sorted({x for x in stream if cms.estimate(x) >= threshold})


if __name__ == "__main__":
    print(bloom_size(10**6, 0.01), round(predicted_false_positive(9586, 7, 1000), 4), round(measured_false_positive(1000, 0.01), 4))
    print(heavy_hitters(["a"] * 50 + ["b"] * 30 + [f"x{i}" for i in range(200)], 25))
