"""Volume 4, Chapter 11 - Bucket Sort: spread evenly distributed keys into buckets, sort each, join.

Run:  python3 ch11_examples.py
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
    """Keys in [lo, hi): bucket i holds keys in the i-th equal slice of the range (Figure 11.2)."""
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


def expected_square(n: int) -> float:
    """E[n_i^2] for one bucket when n keys fall independently and evenly into n buckets: 2 - 1/n (Section 11.5)."""
    return 2 - 1 / n if n > 0 else 0.0


def sum_of_squares(n: int, rng) -> int:
    """Scatter n random keys from [0, 1) into n buckets and return the sum of the squared bucket sizes."""
    sizes = [0] * n
    for _ in range(n):
        sizes[min(int(rng.random() * n), n - 1)] += 1
    return sum(s * s for s in sizes)


SAMPLE = [0.79, 0.82, 0.49, 0.26, 0.0, 0.66, 0.47, 0.76, 0.37, 0.77]   # ten keys for Figure 11.4
SHELF_KEYS = [0.81, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]


def bucket_sizes(keys: list, n: int) -> list:
    """How many keys of [0, 1) fall into each of n equal buckets."""
    sizes = [0] * n
    for x in keys:
        sizes[min(int(x * n), n - 1)] += 1
    return sizes


def average_sum_of_squares(n: int, trials: int, seed: int = 1) -> float:
    """Average of sum(n_i^2) over many scatterings; the theory says n(2 - 1/n) = 2n - 1."""
    rng = random.Random(seed)
    return sum(sum_of_squares(n, rng) for _ in range(trials)) / trials


if __name__ == "__main__":
    log = {}
    print(bucket_sort(PILE, 0, 100, 10, log), log)
    print(experiment())
