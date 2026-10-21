"""Volume 3, Chapter 8 - Selection Sort.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def selection_sort(a: list, passes: list | None = None) -> dict:
    """Sort in place: each pass finds the smallest remaining item and swaps it into place (Figure 8.2).
    Returns counts of comparisons and swaps."""
    comparisons = swaps = 0
    n = len(a)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
        if passes is not None:
            passes.append((i, smallest, list(a)))
    return {"comparisons": comparisons, "swaps": swaps}


def insertion_moves(a: list) -> int:
    """Section 8.8: shifts made by insertion sort, equal to the number of inversions."""
    a = list(a)
    moves = 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
            moves += 1
        a[j + 1] = x
    return moves


def crate_comparison(n: int = 20, trials: int = 200, seed: int = 1) -> tuple[float, float]:
    """Average swaps of selection sort and shifts of insertion sort on random orders."""
    rng = random.Random(seed)
    sel = ins = 0
    for _ in range(trials):
        a = rng.sample(range(1000), n)
        ins += insertion_moves(a)
        sel += selection_sort(list(a))["swaps"]
    return sel / trials, ins / trials


def timed_sort(n: int, seed: int = 1) -> float:
    rng = random.Random(seed)
    a = [rng.random() for _ in range(n)]
    t = time.perf_counter()
    selection_sort(a)
    return (time.perf_counter() - t) * 1e3


if __name__ == "__main__":
    a = PILE[:]
    p = []
    print(selection_sort(a, p))
    for row in p:
        print(row)
    print(selection_sort(sorted(PILE)), selection_sort(sorted(PILE, reverse=True)))
    for n in (1000, 2000, 4000):
        print(n, round(timed_sort(n), 1))
