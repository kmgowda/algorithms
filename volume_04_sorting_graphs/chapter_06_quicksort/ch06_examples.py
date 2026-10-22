"""Volume 4, Chapter 6 - Quicksort.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import random
import sys
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def partition(a: list, lo: int, hi: int, counter: dict | None = None) -> int:
    """Lomuto partition with the last item as pivot: smaller items to the left, pivot between (Figure 6.2)."""
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
    """Sort a[lo..hi] in place: partition around a pivot, then sort each side (Figure 6.3)."""
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


def pair_probability(i: int, j: int) -> float:
    """Chance that the i-th and j-th smallest items (i < j) are ever compared by random-pivot quicksort: they are
    compared exactly when the first pivot chosen from the j - i + 1 items between them is one of the two (Section 6.6)."""
    return 2 / (j - i + 1)


def expected_comparisons(n: int) -> float:
    """Sum of pair_probability over all pairs: exactly 2(n + 1)H(n) - 4n, about 2n ln n = 1.39 n log2 n."""
    return sum(pair_probability(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1))


def closed_form(n: int) -> float:
    harmonic = sum(1 / k for k in range(1, n + 1))
    return 2 * (n + 1) * harmonic - 4 * n


def random_pivot_comparisons(a: list, rng) -> int:
    """Comparisons made by Lomuto quicksort with a pivot chosen uniformly at random (a is sorted in place)."""
    count, stack = 0, [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        k = rng.randint(lo, hi)
        a[k], a[hi] = a[hi], a[k]
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            count += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        stack += [(lo, i - 1), (i + 1, hi)]
    return count


def average_random_pivot(values: list, trials: int, seed: int = 1) -> float:
    rng = random.Random(seed)
    return sum(random_pivot_comparisons(list(values), rng) for _ in range(trials)) / trials


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
