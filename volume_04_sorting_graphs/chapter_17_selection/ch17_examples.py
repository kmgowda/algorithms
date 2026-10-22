"""Volume 4, Chapter 17 - Selection: finding the k-th smallest without sorting everything.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

import heapq
import random

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def partition(a: list, lo: int, hi: int, counter: dict | None = None) -> int:
    """Lomuto partition of a[lo..hi] around the pivot a[hi]; returns the pivot's final position."""
    pivot, i = a[hi], lo
    for j in range(lo, hi):
        if counter is not None:
            counter["comparisons"] += 1
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def quickselect(a: list, k: int, counter: dict | None = None, log: list | None = None, rng=None) -> object:
    """The k-th smallest (k = 1 is the minimum): partition, then keep only the side that holds position k - 1
    (Figure 17.2). Last item as pivot unless rng is given."""
    if not 1 <= k <= len(a):
        raise ValueError("k must be between 1 and len(a)")
    a = list(a)
    lo, hi, target = 0, len(a) - 1, k - 1
    while lo < hi:
        if rng is not None:
            r = rng.randint(lo, hi)
            a[r], a[hi] = a[hi], a[r]
        p = partition(a, lo, hi, counter)
        if log is not None:
            log.append((a[p], p, list(a[lo:hi + 1])))
        if p == target:
            return a[p]
        if target < p:
            hi = p - 1
        else:
            lo = p + 1
    return a[lo]


def median_of_medians(a: list, k: int, counter: dict | None = None) -> object:
    """Guaranteed O(n) selection: pivot = median of the medians of groups of five (Section 17.6)."""
    if len(a) <= 5:
        if counter is not None:
            counter["comparisons"] += len(a) * (len(a) - 1) // 2
        return sorted(a)[k - 1]
    groups = [a[i:i + 5] for i in range(0, len(a), 5)]
    meds = []
    for g in groups:
        if counter is not None:
            counter["comparisons"] += len(g) * (len(g) - 1) // 2
        meds.append(sorted(g)[(len(g) - 1) // 2])
    pivot = median_of_medians(meds, (len(meds) + 1) // 2, counter)
    if counter is not None:
        counter["comparisons"] += 2 * len(a)
    smaller = [x for x in a if x < pivot]
    equal = [x for x in a if x == pivot]
    larger = [x for x in a if x > pivot]
    if k <= len(smaller):
        return median_of_medians(smaller, k, counter)
    if k <= len(smaller) + len(equal):
        return pivot
    return median_of_medians(larger, k - len(smaller) - len(equal), counter)


def mom_pivot(a: list) -> tuple[list, object]:
    """One round of median of medians (Figure 17.5): the groups of five, each sorted, and the pivot chosen."""
    groups = [sorted(a[i:i + 5]) for i in range(0, len(a), 5)]
    meds = [g[(len(g) - 1) // 2] for g in groups]
    return groups, median_of_medians(meds, (len(meds) + 1) // 2)


def guaranteed_side(n: int) -> int:
    """Items certainly larger than the median-of-medians pivot (and, likewise, smaller): at least 3 from each of the
    groups whose median is above the pivot's, leaving out the pivot's own group and a short last group."""
    import math
    return max(0, 3 * (math.ceil(math.ceil(n / 5) / 2) - 2))


def expected_select(n_max: int) -> list:
    """E[n][k]: the exact average comparisons of random-pivot quickselect (Lomuto, n - 1 comparisons per partition)
    for the k-th smallest of n distinct items, for every n <= n_max (Section 17.5)."""
    E = [[0.0] * (n_max + 2) for _ in range(n_max + 2)]
    for n in range(2, n_max + 1):
        for k in range(1, n + 1):
            total = sum(E[n - p][k - p] for p in range(1, k)) + sum(E[p - 1][k] for p in range(k + 1, n + 1))
            E[n][k] = n - 1 + total / n
    return E


def average_median_comparisons(n: int, runs: int, seed: int = 1) -> float:
    """Measured comparisons per item of random-pivot quickselect for the median of n random numbers."""
    rng = random.Random(seed)
    a = [rng.random() for _ in range(n)]
    total = 0
    for r in range(runs):
        c = {"comparisons": 0}
        quickselect(a, n // 2, c, rng=random.Random(seed * 1000 + r))
        total += c["comparisons"]
    return total / runs / n


def smallest_k_heap(a: list, k: int) -> list:
    """The k smallest, in order, with a max-heap of size k (Volume 3, Chapter 15): O(n log k)."""
    return heapq.nsmallest(k, a)


def comparisons_table(n: int = 100_000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    a = [rng.random() for _ in range(n)]
    out = {}
    c = {"comparisons": 0}; quickselect(a, n // 2, c, rng=random.Random(2)); out["quickselect (random pivot)"] = c["comparisons"]
    c = {"comparisons": 0}; median_of_medians(a, n // 2, c); out["median of medians"] = c["comparisons"]
    import math
    out["sorting first (about n log2 n)"] = round(n * math.log2(n))
    return out


if __name__ == "__main__":
    c, log = {"comparisons": 0}, []
    print(quickselect(PILE, 5, c, log), c)
    for row in log:
        print(row)
    for k in (1, 9, 3):
        c = {"comparisons": 0}; print(k, quickselect(PILE, k, c), c)
    c = {"comparisons": 0}; print("sorted median", quickselect(sorted(PILE), 5, c), c)
    print(median_of_medians(PILE, 5), smallest_k_heap(PILE, 3))
    print(comparisons_table())
