"""Volume 1, Chapter 24 - Comparing Searches: every search of Part IV on the same catalogue.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

import bisect
import random
import time


def linear_looks(a: list, key) -> int:
    for i, v in enumerate(a):
        if v == key:
            return i + 1
    return len(a)


def binary_looks(a: list, key) -> int:
    lo, hi, looks = 0, len(a), 0
    while lo < hi:
        mid = (lo + hi) // 2
        looks += 1
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    return looks + 1                     # one final look to confirm


def exponential_looks(a: list, key) -> int:
    looks, hi = 0, 1
    while hi < len(a) and a[hi] < key:
        looks += 1
        hi *= 2
    looks += 1
    return looks + binary_looks(a[hi // 2:min(hi, len(a)) + 1], key)


def interpolation_looks(a: list, key) -> int:
    lo, hi, looks = 0, len(a) - 1, 0
    while lo <= hi and a[lo] <= key <= a[hi]:
        pos = lo if a[hi] == a[lo] else lo + (key - a[lo]) * (hi - lo) // (a[hi] - a[lo])
        looks += 1
        if a[pos] == key:
            return looks
        if a[pos] < key:
            lo = pos + 1
        else:
            hi = pos - 1
    return max(looks, 1)


def experiment(n: int = 1_000_000, queries: int = 1000, seed: int = 1) -> dict:
    """Average looks and total time for the same queries on the same sorted catalogue."""
    rng = random.Random(seed)
    a = sorted(rng.sample(range(10 * n), n))
    keys = rng.sample(a, queries)
    lin_keys = keys[:50]                                   # linear search is too slow for all of them
    s = set(a)
    out = {}
    out["linear"] = (sum(linear_looks(a, k) for k in lin_keys) / len(lin_keys), None)
    out["binary"] = (sum(binary_looks(a, k) for k in keys) / queries, None)
    out["exponential"] = (sum(exponential_looks(a, k) for k in keys) / queries, None)
    out["interpolation"] = (sum(interpolation_looks(a, k) for k in keys) / queries, None)
    out["hash set"] = (1.0, None)
    t = time.perf_counter(); [k in a for k in lin_keys]; lin = (time.perf_counter() - t) / len(lin_keys) * queries
    t = time.perf_counter(); [bisect.bisect_left(a, k) for k in keys]; bis = time.perf_counter() - t
    t = time.perf_counter(); [k in s for k in keys]; hs = time.perf_counter() - t
    out["times ms"] = {"linear (estimated)": lin * 1e3, "binary (bisect)": bis * 1e3, "hash set": hs * 1e3}
    return out


if __name__ == "__main__":
    for k, v in experiment().items():
        print(k, v)
