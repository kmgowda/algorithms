"""Volume 4, Chapter 10 - Quicksort in Practice: better pivots, three-way partitioning, and small pieces.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import random
import sys
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def quicksort_random(a: list, lo: int = 0, hi: int | None = None, rng=None, counter: dict | None = None) -> None:
    """Quicksort with a random pivot (Section 10.4): no input order is reliably bad."""
    if hi is None:
        hi, rng = len(a) - 1, rng or random.Random(1)
    while lo < hi:
        k = rng.randint(lo, hi)
        a[k], a[hi] = a[hi], a[k]
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            if counter is not None:
                counter["comparisons"] += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        if i - lo < hi - i:                       # recurse into the smaller side: depth O(log n)
            quicksort_random(a, lo, i - 1, rng, counter)
            lo = i + 1
        else:
            quicksort_random(a, i + 1, hi, rng, counter)
            hi = i - 1


def median_of_three(a: list, lo: int, hi: int) -> int:
    """Index of the median of the first, middle and last items (Figure 10.1)."""
    mid = (lo + hi) // 2
    trio = sorted([(a[lo], lo), (a[mid], mid), (a[hi], hi)])
    return trio[1][1]


def partition3(a: list, lo: int, hi: int, counter: dict | None = None) -> tuple[int, int]:
    """Dutch national flag: < pivot | = pivot | > pivot (Figure 10.2). Returns the bounds of the middle part."""
    pivot = a[median_of_three(a, lo, hi)]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if counter is not None:
            counter["comparisons"] += 1
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def insertion_range(a: list, lo: int, hi: int) -> None:
    for i in range(lo + 1, hi + 1):
        x, j = a[i], i - 1
        while j >= lo and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def quicksort_practical(a: list, lo: int = 0, hi: int | None = None, cutoff: int = 16,
                        counter: dict | None = None) -> None:
    """Median-of-three pivot, three-way partition, insertion sort for small pieces, smaller side first."""
    if hi is None:
        hi = len(a) - 1
    while hi - lo + 1 > cutoff:
        lt, gt = partition3(a, lo, hi, counter)
        if lt - lo < hi - gt:
            quicksort_practical(a, lo, lt - 1, cutoff, counter)
            lo = gt + 1
        else:
            quicksort_practical(a, gt + 1, hi, cutoff, counter)
            hi = lt - 1
    insertion_range(a, lo, hi)


def lomuto_last(a: list, lo: int = 0, hi: int | None = None) -> None:
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    pivot, i = a[hi], lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    lomuto_last(a, lo, i - 1)
    lomuto_last(a, i + 1, hi)


def hoare_partition(a: list, lo: int, hi: int, counter: dict | None = None, log: list | None = None) -> int:
    """Hoare's partition around the value in the middle position (Section 10.5). Two fingers move towards each other
    and swap a pair that is on the wrong sides. Returns j with every item of a[lo..j] <= pivot <= every item of
    a[j+1..hi]; the pivot itself need not end at j."""
    pivot = a[(lo + hi) // 2]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            if counter is not None:
                counter["comparisons"] += 1
            i += 1
        j -= 1
        while a[j] > pivot:
            if counter is not None:
                counter["comparisons"] += 1
            j -= 1
        if counter is not None:
            counter["comparisons"] += 2          # the two comparisons that stopped the fingers
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]
        if counter is not None:
            counter["swaps"] += 1
        if log is not None:
            log.append((i, j, list(a[lo:hi + 1])))


def quicksort_hoare(a: list, lo: int = 0, hi: int | None = None, counter: dict | None = None) -> None:
    """Quicksort with Hoare's partition: recurse on lo..j and j+1..hi."""
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    j = hoare_partition(a, lo, hi, counter)
    quicksort_hoare(a, lo, j, counter)
    quicksort_hoare(a, j + 1, hi, counter)


def lomuto_counts(a: list) -> dict:
    """Comparisons and swaps of last-item Lomuto quicksort (Chapter 9), for comparison with Hoare's scheme."""
    c = {"comparisons": 0, "swaps": 0}

    def sort(lo, hi):
        if lo >= hi:
            return
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            c["comparisons"] += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                c["swaps"] += 1
                i += 1
        a[i], a[hi] = a[hi], a[i]
        c["swaps"] += 1
        sort(lo, i - 1)
        sort(i + 1, hi)
    sort(0, len(a) - 1)
    return c


def timing_random(n: int = 100_000, seed: int = 1) -> float:
    """Milliseconds for the practical quicksort on n random numbers (the comparison table of Chapter 11, Section 11.5)."""
    rng = random.Random(seed)
    a = [rng.random() for _ in range(n)]
    t = time.perf_counter()
    quicksort_practical(a)
    return round((time.perf_counter() - t) * 1e3)


def compare(n: int = 4000, seed: int = 1) -> dict:
    """The timing table of Section 10.7: milliseconds for three quicksorts on four kinds of input."""
    rng = random.Random(seed)
    inputs = {"random": [rng.random() for _ in range(n)], "sorted": sorted(rng.random() for _ in range(n)),
              "all equal": [7] * n, "few values": [rng.randint(1, 5) for _ in range(n)]}
    out = {}
    for name, data in inputs.items():
        row = {}
        for label, fn in (("last item", lomuto_last), ("random pivot", quicksort_random),
                          ("practical", quicksort_practical)):
            a = list(data)
            t = time.perf_counter()
            fn(a)
            row[label] = round((time.perf_counter() - t) * 1e3, 1)
            assert a == sorted(data)
        out[name] = row
    return out


def fisher_yates(a: list, rng=random) -> list:
    """Shuffle in place so that all n! orders are equally likely: for i from the end down to 1, swap a[i] with a
    position chosen uniformly from 0..i (Fisher and Yates, 1938; Durstenfeld's in-place form, 1964)."""
    for i in range(len(a) - 1, 0, -1):
        j = rng.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return a


def shuffle_outcomes(n: int, naive: bool = False) -> dict:
    """Count how often each order appears over every possible sequence of choices: Fisher-Yates (j from 0..i)
    against the naive shuffle (every position i swapped with any j from 0..n-1)."""
    import itertools
    steps = list(range(n)) if naive else list(range(n - 1, 0, -1))
    ranges = [range(n) if naive else range(i + 1) for i in steps]
    counts = {}
    for choice in itertools.product(*ranges):
        a = list(range(n))
        for i, j in zip(steps, choice):
            a[i], a[j] = a[j], a[i]
        counts[tuple(a)] = counts.get(tuple(a), 0) + 1
    return counts


if __name__ == "__main__":
    sys.setrecursionlimit(20_000)
    a = list(PILE)
    print(median_of_three(a, 0, 8), a[median_of_three(a, 0, 8)])
    b = [3, 1, 3, 2, 3, 1, 2, 3]
    print(partition3(b, 0, 7), b)
    for k, v in compare().items():
        print(k, v)
    print(fisher_yates(list(PILE), random.Random(10)), shuffle_outcomes(3, naive=True))
