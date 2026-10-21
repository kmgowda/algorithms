"""Volume 3, Chapter 11 - Merge Sort.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def merge(left: list, right: list, counter: dict | None = None) -> list:
    """Merge two sorted lists: repeatedly take the smaller front item (Figure 11.3). Stable: ties take from left."""
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if counter is not None:
            counter["comparisons"] += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def merge_sort(a: list, counter: dict | None = None, log: list | None = None, depth: int = 0) -> list:
    """Split in half, sort each half, merge (Figure 11.2). Returns a new sorted list."""
    if log is not None:
        log.append(("split", depth, list(a)))
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left = merge_sort(a[:mid], counter, log, depth + 1)
    right = merge_sort(a[mid:], counter, log, depth + 1)
    out = merge(left, right, counter)
    if log is not None:
        log.append(("merge", depth, out))
    return out


def merge_branch_lists(lists: list[list], counter: dict | None = None) -> list:
    """Section 11.9: merge already-sorted lists in pairs, level by level."""
    while len(lists) > 1:
        lists = [merge(lists[i], lists[i + 1], counter) if i + 1 < len(lists) else lists[i]
                 for i in range(0, len(lists), 2)]
    return lists[0] if lists else []


def timing(ns=(10_000, 100_000), seed: int = 1) -> dict:
    out = {}
    for n in ns:
        rng = random.Random(seed)
        a = [rng.random() for _ in range(n)]
        t = time.perf_counter(); merge_sort(a); ms = (time.perf_counter() - t) * 1e3
        c = {"comparisons": 0}; merge_sort(a, c)
        out[n] = (round(ms, 1), c["comparisons"])
    return out


if __name__ == "__main__":
    c = {"comparisons": 0}
    log = []
    print(merge_sort(PILE, c, log), c)
    for e in log:
        if e[0] == "merge":
            print(e)
    c = {"comparisons": 0}; merge([12, 25, 58, 91], [31, 47, 63, 70, 84], c); print(c)
    print(timing())
