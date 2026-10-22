"""Volume 2, Chapter 24 - Comparing Hashing, Sorting, and Searching.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

import bisect
import random
import timeit


def present_unsorted(items: list[int], x: int) -> bool:
    return x in items                     # Python scans the list item by item


def present_sorted(items: list[int], x: int) -> bool:
    i = bisect.bisect_left(items, x)
    return i < len(items) and items[i] == x


def range_sorted(items: list[int], a: int, b: int) -> list[int]:
    """All items between a and b: binary search to a, then walk (O(log n + k))."""
    return items[bisect.bisect_left(items, a):bisect.bisect_right(items, b)]


def range_hashed(items: set[int], a: int, b: int) -> list[int]:
    """A hash set must check every item (O(n))."""
    return sorted(x for x in items if a <= x <= b)


def measure(n: int = 100_000, seed: int = 1) -> dict[str, float]:
    """Milliseconds for the experiments of Figure 24.3, best of 3."""
    rng = random.Random(seed)
    data = rng.sample(range(10 ** 7), n)
    queries = rng.sample(range(10 ** 7), 1000)
    srt, st = sorted(data), set(data)
    best = lambda f, number=1: min(timeit.repeat(f, number=number, repeat=3)) * 1000 / number  # noqa: E731
    return {
        "1000 lookups: unsorted list": best(lambda: [present_unsorted(data, q) for q in queries[:100]]) * 10,
        "1000 lookups: sorted + bisect": best(lambda: [present_sorted(srt, q) for q in queries]),
        "1000 lookups: hash set": best(lambda: [q in st for q in queries]),
        "100 ranges: sorted + bisect": best(lambda: [range_sorted(srt, q, q + 10_000) for q in queries[:100]]),
        "100 ranges: hash set": best(lambda: [range_hashed(st, q, q + 10_000) for q in queries[:10]]) * 10,
        "build: sort": best(lambda: sorted(data)),
        "build: set": best(lambda: set(data)),
    }


if __name__ == "__main__":
    for k, v in measure().items():
        print(f"{k:32s} {v:10.3f} ms")
