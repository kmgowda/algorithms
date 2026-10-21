"""Volume 3, Chapter 18 - Stability and Timsort: sorting real data, which is rarely random.

A teaching version of Timsort: find natural runs (reversing falling ones), extend short runs with insertion sort,
and merge runs from a stack while keeping run lengths balanced. (Python's own sorted() is the full Timsort, with
galloping; this version omits galloping to stay short.)

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def find_runs(a: list, counter: dict | None = None) -> list[tuple[int, int]]:
    """Split a into maximal rising (non-decreasing) runs; a strictly falling run is reversed in place (Figure 18.2)."""
    runs, i, n = [], 0, len(a)
    while i < n:
        j = i + 1
        if j < n:
            if counter is not None:
                counter["comparisons"] += 1
            if a[j] < a[i]:                                   # strictly falling: extend, then reverse
                while j + 1 < n and a[j + 1] < a[j]:
                    if counter is not None:
                        counter["comparisons"] += 1
                    j += 1
                if counter is not None and j + 1 < n:
                    counter["comparisons"] += 1
                j += 1
                a[i:j] = a[i:j][::-1]
            else:
                while j + 1 < n and a[j + 1] >= a[j]:
                    if counter is not None:
                        counter["comparisons"] += 1
                    j += 1
                if counter is not None and j + 1 < n:
                    counter["comparisons"] += 1
                j += 1
        runs.append((i, j))
        i = j
    return runs


def merge(a: list, lo: int, mid: int, hi: int, counter: dict | None = None) -> None:
    left, right = a[lo:mid], a[mid:hi]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if counter is not None:
            counter["comparisons"] += 1
        if left[i] <= right[j]:                       # ties from the left: stable
            a[k] = left[i]; i += 1
        else:
            a[k] = right[j]; j += 1
        k += 1
    a[k:hi] = left[i:] + right[j:]


def timsort(a: list, counter: dict | None = None, log: list | None = None) -> None:
    """Sort a in place by merging natural runs, smaller neighbours first."""
    runs = find_runs(a, counter)
    if log is not None:
        log.append(("runs", [a[s:e] for s, e in runs]))
    stack: list[tuple[int, int]] = []
    for run in runs:
        stack.append(run)
        while len(stack) >= 2 and (stack[-2][1] - stack[-2][0]) <= (stack[-1][1] - stack[-1][0]):
            (s1, e1), (s2, e2) = stack[-2], stack.pop()
            merge(a, s1, e1, e2, counter)
            stack[-1] = (s1, e2)
            if log is not None:
                log.append(("merge", a[s1:e2]))
    while len(stack) >= 2:
        (s1, e1), (s2, e2) = stack[-2], stack.pop()
        merge(a, s1, e1, e2, counter)
        stack[-1] = (s1, e2)
        if log is not None:
            log.append(("merge", a[s1:e2]))


def merge_sort_comparisons(a: list) -> int:
    c = {"comparisons": 0}

    def ms(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        ms(lo, mid)
        ms(mid, hi)
        merge(b, lo, mid, hi, c)
    b = list(a)
    ms(0, len(b))
    return c["comparisons"]


def builtin_timing(n: int = 1_000_000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    base = [rng.random() for _ in range(n)]
    nearly = sorted(base)
    for _ in range(n // 1000):
        i, j = rng.randrange(n), rng.randrange(n)
        nearly[i], nearly[j] = nearly[j], nearly[i]
    runs = []
    for k in range(10):
        runs += sorted(base[k * n // 10:(k + 1) * n // 10])
    out = {}
    for name, data in (("random", base), ("sorted", sorted(base)), ("reversed", sorted(base, reverse=True)),
                       ("nearly sorted (0.1% swapped)", nearly), ("ten sorted runs", runs)):
        t = time.perf_counter()
        sorted(data)
        out[name] = round((time.perf_counter() - t) * 1e3, 1)
    return out


if __name__ == "__main__":
    a, c, log = list(PILE), {"comparisons": 0}, []
    timsort(a, c, log)
    print(a, c, log)
    for name, data in (("sorted", list(range(1, 17))), ("reversed", list(range(16, 0, -1))),
                       ("two runs", [3, 8, 12, 15, 21, 27, 30, 34, 2, 5, 9, 14, 18, 22, 25, 33])):
        c = {"comparisons": 0}
        b = list(data)
        timsort(b, c)
        print(name, c, merge_sort_comparisons(data), b == sorted(data))
    print(builtin_timing())
