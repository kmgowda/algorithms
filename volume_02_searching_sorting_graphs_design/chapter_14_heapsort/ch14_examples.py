"""Volume 2, Chapter 14 - Heapsort.

Run:  python3 ch14_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def sift_down(a: list, i: int, n: int, counter: dict | None = None) -> None:
    """Move a[i] down a max-heap of size n until both children are smaller (Volume 1, Chapter 54, mirrored)."""
    while True:
        big, l, r = i, 2 * i + 1, 2 * i + 2
        if l < n:
            if counter is not None:
                counter["comparisons"] += 1
            if a[l] > a[big]:
                big = l
        if r < n:
            if counter is not None:
                counter["comparisons"] += 1
            if a[r] > a[big]:
                big = r
        if big == i:
            return
        a[i], a[big] = a[big], a[i]
        i = big


def heapsort(a: list, counter: dict | None = None, log: list | None = None) -> None:
    """Build a max-heap in place, then repeatedly swap the largest to the end and repair (Figures 14.2-14.3)."""
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n, counter)
    if log is not None:
        log.append(("heap", list(a)))
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end, counter)
        if log is not None:
            log.append((a[end], list(a)))


def top_k_by_heapsort(a: list, k: int, counter: dict | None = None) -> list:
    """Section 14.6: build a max-heap, then run only k rounds of phase 2; returns the k largest, largest first."""
    a = list(a)
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n, counter)
    for end in range(n - 1, n - 1 - k, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end, counter)
    return a[n - k:][::-1]


def timing(n: int = 100_000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    base = [rng.random() for _ in range(n)]
    out = {}
    for name, data in (("random", base), ("sorted", sorted(base)), ("reversed", sorted(base, reverse=True))):
        a = list(data)
        c = {"comparisons": 0}
        t = time.perf_counter()
        heapsort(a, c)
        out[name] = (round((time.perf_counter() - t) * 1e3), c["comparisons"])
    return out


if __name__ == "__main__":
    a, c, log = list(PILE), {"comparisons": 0}, []
    heapsort(a, c, log)
    print(a, c)
    for e in log[:5]:
        print(e)
    print(timing())
