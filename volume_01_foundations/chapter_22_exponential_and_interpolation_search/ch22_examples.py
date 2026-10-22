"""Volume 1, Chapter 22 - Exponential and Interpolation Search.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

import random


class Reel:
    """A sorted sequence whose length is unknown: reading past the end returns None (the microfilm reel)."""

    def __init__(self, values):
        self._v = list(values)
        self.reads = 0

    def read(self, i):
        self.reads += 1
        return self._v[i] if i < len(self._v) else None


def exponential_search(reel: Reel, key, trace: list | None = None) -> int:
    """Gallop 1, 2, 4, 8, ... until passing the key or the end, then binary search the last gap (Figure 22.2)."""
    hi = 1
    while True:
        v = reel.read(hi)
        if trace is not None:
            trace.append(("gallop", hi, v))
        if v is None or v >= key:
            break
        hi *= 2
    lo = hi // 2
    while lo < hi:                                  # lower bound in [lo, hi): reading past the end counts as "large"
        mid = (lo + hi) // 2
        v = reel.read(mid)
        if trace is not None:
            trace.append(("binary", mid, v))
        if v is not None and v < key:
            lo = mid + 1
        else:
            hi = mid
    v = reel.read(lo)
    return lo if v == key else -1


def interpolation_search(a: list, key, trace: list | None = None) -> int:
    """Guess the position from the value, as with a phone book (Figure 22.4)."""
    lo, hi = 0, len(a) - 1
    while lo <= hi and a[lo] <= key <= a[hi]:
        if a[hi] == a[lo]:
            pos = lo
        else:
            pos = lo + (key - a[lo]) * (hi - lo) // (a[hi] - a[lo])
        if trace is not None:
            trace.append((lo, hi, pos, a[pos]))
        if a[pos] == key:
            return pos
        if a[pos] < key:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


def binary_looks(a: list, key) -> int:
    lo, hi, looks = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        looks += 1
        if a[mid] == key:
            break
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return looks


def average_looks(a: list, keys: list) -> tuple[float, float]:
    inter = 0
    for k in keys:
        t = []
        interpolation_search(a, k, t)
        inter += len(t)
    return sum(binary_looks(a, k) for k in keys) / len(keys), inter / len(keys)


if __name__ == "__main__":
    reel = Reel(range(3, 3000, 3))           # 999 entries: 3, 6, 9, ...
    t = []
    print(exponential_search(reel, 87, t), t, reel.reads)
    shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
    t = []
    print(interpolation_search(shelf, 70, t), t)
    rng = random.Random(1)
    uniform = sorted(rng.sample(range(10_000_000), 1_000_000))
    keys = rng.sample(uniform, 2000)
    print("uniform", average_looks(uniform, keys))
    skewed = [i ** 4 for i in range(1, 1_000_001)]          # distinct, but bunched near the start
    keys = rng.sample(skewed, 2000)
    print("skewed", average_looks(skewed, keys))
