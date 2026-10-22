"""Volume 4, Chapter 4 - Bubble Sort and Shell Sort.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def bubble_sort(a: list, passes: list | None = None) -> dict:
    """Swap neighbours that are out of order; stop after a pass with no swaps (Figure 4.1)."""
    comparisons = swaps = 0
    n = len(a)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swaps += 1
                swapped = True
        if passes is not None:
            passes.append(list(a))
        if not swapped:
            break
    return {"comparisons": comparisons, "swaps": swaps}


def knuth_gaps(n: int) -> list[int]:
    """The gaps 1, 4, 13, 40, ... (each three times the last plus one) below n, largest first."""
    gaps, g = [], 1
    while g < n:
        gaps.insert(0, g)
        g = 3 * g + 1
    return gaps


def shell_sort(a: list, gaps=None, rounds: list | None = None) -> dict:
    """Insertion sort on items a gap apart, for shrinking gaps ending with 1 (Figure 4.2)."""
    n = len(a)
    gaps = knuth_gaps(n) if gaps is None else gaps
    comparisons = shifts = 0
    for gap in gaps:
        for i in range(gap, n):
            x, j = a[i], i
            while j >= gap:
                comparisons += 1
                if a[j - gap] <= x:
                    break
                a[j] = a[j - gap]
                shifts += 1
                j -= gap
            a[j] = x
        if rounds is not None:
            rounds.append((gap, list(a)))
    return {"comparisons": comparisons, "shifts": shifts}


def insertion_sort(a: list) -> None:
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def mixup_timing(n: int = 5000, seed: int = 1) -> dict:
    """Section 4.8: comparisons for neighbour swaps versus a few far-moved books."""
    rng = random.Random(seed)
    near = list(range(n))
    for _ in range(5):
        i = rng.randrange(n - 1)
        near[i], near[i + 1] = near[i + 1], near[i]
    far = list(range(n))
    for _ in range(5):
        far.append(far.pop(rng.randrange(n // 10)))          # small books moved to the far end
    out = {}
    for name, data in (("near", near), ("far", far)):
        out[name] = {"bubble": bubble_sort(list(data))["comparisons"], "shell": shell_sort(list(data))["comparisons"]}
    return out


def timing(ns=(2000, 4000), seed: int = 1) -> dict:
    out = {}
    for n in ns:
        rng = random.Random(seed)
        base = [rng.random() for _ in range(n)]
        row = {}
        for name, fn in (("bubble", bubble_sort), ("insertion", insertion_sort), ("shell", shell_sort)):
            a = list(base)
            t = time.perf_counter()
            fn(a)
            row[name] = round((time.perf_counter() - t) * 1e3, 1)
        out[n] = row
    return out


if __name__ == "__main__":
    a = list(PILE)
    p = []
    print(bubble_sort(a, p))
    for row in p:
        print(row)
    print(bubble_sort(sorted(PILE)))
    a = list(PILE)
    r = []
    print(shell_sort(a, [4, 1], r), r)
    print(timing())
    rng = random.Random(1)
    big = [rng.random() for _ in range(100_000)]
    t = time.perf_counter(); shell_sort(big); print("shell 100k ms", round((time.perf_counter() - t) * 1e3))
