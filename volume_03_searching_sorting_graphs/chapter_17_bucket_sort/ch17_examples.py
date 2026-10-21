"""Volume 3, Chapter 17 - Bucket Sort: spread evenly distributed keys into buckets, sort each, join.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

import random

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def insertion_sort(a: list) -> int:
    """Sort a in place; return the number of comparisons."""
    comps = 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0:
            comps += 1
            if a[j] <= x:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return comps


def bucket_sort(a: list, lo: float, hi: float, nbuckets: int | None = None, log: dict | None = None) -> list:
    """Keys in [lo, hi): bucket i holds keys in the i-th equal slice of the range (Figure 17.2)."""
    n = len(a)
    if n == 0:
        return []
    m = nbuckets or n
    buckets = [[] for _ in range(m)]
    width = (hi - lo) / m
    for x in a:
        i = min(int((x - lo) / width), m - 1)
        buckets[i].append(x)
    comps = 0
    for b in buckets:
        comps += insertion_sort(b)
    if log is not None:
        log["buckets"] = [list(b) for b in buckets]
        log["comparisons"] = comps
    return [x for b in buckets for x in b]


def experiment(n: int = 10_000, seed: int = 1) -> dict:
    """Comparisons inside the buckets for even and for bunched keys."""
    rng = random.Random(seed)
    out = {}
    for name, data in (("even", [rng.random() for _ in range(n)]),
                       ("bunched", [rng.random() ** 8 for _ in range(n)])):
        log = {}
        bucket_sort(data, 0.0, 1.0, log=log)
        sizes = [len(b) for b in log["buckets"]]
        out[name] = (log["comparisons"], max(sizes), sum(1 for s in sizes if s == 0))
    return out


if __name__ == "__main__":
    log = {}
    print(bucket_sort(PILE, 0, 100, 10, log), log)
    print(experiment())
