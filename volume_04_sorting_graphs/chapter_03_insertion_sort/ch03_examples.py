"""Volume 4, Chapter 3 - Insertion Sort.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def insertion_sort(a: list, steps: list | None = None) -> dict:
    """Sort in place: take each item and slide it left past larger items (Figure 3.2).
    Returns counts of comparisons and shifts."""
    comparisons = shifts = 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0:
            comparisons += 1
            if a[j] <= x:
                break
            a[j + 1] = a[j]                 # shift the larger item one place right
            shifts += 1
            j -= 1
        a[j + 1] = x
        if steps is not None:
            steps.append((x, j + 1, list(a)))
    return {"comparisons": comparisons, "shifts": shifts}


def nightly_catalogue(n: int = 20_000, new: int = 50, near_end: bool = True, seed: int = 1) -> dict:
    """Section 3.8: a sorted catalogue plus new entries appended at the end, re-sorted by insertion sort."""
    rng = random.Random(seed)
    cat = sorted(rng.sample(range(10 * n), n))
    if near_end:
        extra = [cat[-1] - rng.randint(0, 200) for _ in range(new)]
    else:
        extra = [rng.randrange(10 * n) for _ in range(new)]
    return insertion_sort(cat + extra)


def timed(values: list) -> float:
    a = list(values)
    t = time.perf_counter()
    insertion_sort(a)
    return (time.perf_counter() - t) * 1e3


def timing_table(n: int = 2000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    rand = [rng.random() for _ in range(n)]
    nearly = sorted(rand)
    for _ in range(n // 100):                      # 1% of items swapped with a neighbour
        i = rng.randrange(n - 1)
        nearly[i], nearly[i + 1] = nearly[i + 1], nearly[i]
    return {"sorted": timed(sorted(rand)), "nearly sorted": timed(nearly), "random": timed(rand),
            "reversed": timed(sorted(rand, reverse=True))}


if __name__ == "__main__":
    a = list(PILE)
    s = []
    print(insertion_sort(a, s))
    for row in s:
        print(row)
    print(insertion_sort(sorted(PILE)), insertion_sort(sorted(PILE, reverse=True)))
    print({k: round(v, 2) for k, v in timing_table().items()})
