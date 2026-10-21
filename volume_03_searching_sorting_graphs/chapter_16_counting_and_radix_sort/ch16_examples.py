"""Volume 3, Chapter 16 - Counting Sort and Radix Sort: sorting without comparing.

Run:  python3 ch16_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]
GRADES = [3, 1, 4, 1, 5, 2, 4, 3, 1, 5, 2, 4]            # books borrowed by twelve readers (0..5)


def counting_sort(a: list, k: int, key=lambda x: x, steps: dict | None = None) -> list:
    """Stable counting sort of items whose key is 0..k (Figure 16.2): count, prefix-sum, place from the right."""
    count = [0] * (k + 1)
    for x in a:
        count[key(x)] += 1
    if steps is not None:
        steps["counts"] = list(count)
    for v in range(1, k + 1):
        count[v] += count[v - 1]                      # count[v] = how many keys are <= v
    if steps is not None:
        steps["ends"] = list(count)
    out = [None] * len(a)
    for x in reversed(a):                             # right to left keeps equal keys in order: stable
        count[key(x)] -= 1
        out[count[key(x)]] = x
    return out


def radix_sort(a: list, digits: int, base: int = 10, passes: list | None = None) -> list:
    """Least-significant-digit radix sort: one stable counting sort per digit (Figure 16.4)."""
    for d in range(digits):
        div = base ** d
        a = counting_sort(a, base - 1, key=lambda x: (x // div) % base)
        if passes is not None:
            passes.append(list(a))
    return a


def step_counts(n: int, k: int, digits: int, base: int = 10) -> dict:
    """Basic steps (reads and writes of one item or one counter) for each method, against comparisons for a
    comparison sort (Section 16.6)."""
    import math
    return {"counting sort": 2 * n + 2 * (k + 1), "radix sort": digits * (2 * n + 2 * base),
            "comparison sort (about n log2 n)": round(n * math.log2(n)) if n > 1 else 0}


def counting_sort_any(a: list) -> list:
    """Section 16.7: counting sort for any whole numbers, including negatives, by shifting keys to start at 0."""
    if not a:
        return []
    lo, hi = min(a), max(a)
    return counting_sort(a, hi - lo, key=lambda x: x - lo)


def timing(n: int = 1_000_000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    small = [rng.randint(0, 100) for _ in range(n)]
    six = [rng.randint(0, 999_999) for _ in range(n)]
    out = {}
    t = time.perf_counter(); counting_sort(small, 100); out["counting, keys 0-100"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); radix_sort(six, 6); out["radix, 6-digit keys"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); sorted(small); out["sorted(), keys 0-100"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); sorted(six); out["sorted(), 6-digit keys"] = (time.perf_counter() - t) * 1e3
    return {k: round(v) for k, v in out.items()}


if __name__ == "__main__":
    s = {}
    print(counting_sort(GRADES, 5, steps=s), s)
    p = []
    print(radix_sort(PILE, 2, passes=p), p)
    print(timing())
