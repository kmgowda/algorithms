"""Volume 3, Chapter 12 - Quicksort.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import random
import sys
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def partition(a: list, lo: int, hi: int, counter: dict | None = None) -> int:
    """Lomuto partition with the last item as pivot: smaller items to the left, pivot between (Figure 12.2)."""
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if counter is not None:
            counter["comparisons"] += 1
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def quicksort(a: list, lo: int = 0, hi: int | None = None, counter: dict | None = None,
              log: list | None = None, depth: int = 0) -> None:
    """Sort a[lo..hi] in place: partition around a pivot, then sort each side (Figure 12.3)."""
    if hi is None:
        hi = len(a) - 1
    if counter is not None:
        counter["max_depth"] = max(counter.get("max_depth", 0), depth)
    if lo >= hi:
        return
    p = partition(a, lo, hi, counter)
    if log is not None:
        log.append((depth, a[p], list(a[lo:p]), list(a[p + 1:hi + 1])))
    quicksort(a, lo, p - 1, counter, log, depth + 1)
    quicksort(a, p + 1, hi, counter, log, depth + 1)


def measure(values: list) -> tuple[float, int, int]:
    a = list(values)
    c = {"comparisons": 0}
    t = time.perf_counter()
    quicksort(a, counter=c)
    return round((time.perf_counter() - t) * 1e3, 1), c["comparisons"], c["max_depth"]


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    a = list(PILE)
    c = {"comparisons": 0}
    log = []
    quicksort(a, counter=c, log=log)
    print(a, c)
    for e in log:
        print(e)
    rng = random.Random(1)
    for n in (1000, 2000, 4000):
        r = [rng.random() for _ in range(n)]
        print(n, "random", measure(r), "sorted", measure(sorted(r)))
