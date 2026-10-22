"""Volume 7, Chapter 32 - Thinking Problems.

Problem 1: the tree sum of n >= 1 values takes exactly ceil(log2 n) rounds and n - 1 additions (checked).
Problem 2: a parallel filter: keep the values above a threshold, in order, with O(n) work and O(log n) span, by a scan.
Problem 3: updating the scan in place lets a round read values it has already changed: wrong totals.
"""

from __future__ import annotations

import math

from ch32_examples import prefix_sums_parallel


def rounds_predicted(n: int) -> int:
    return 0 if n <= 1 else math.ceil(math.log2(n))


def parallel_filter(values: list, threshold) -> tuple[list, int]:
    """flags (all at once) -> scan of flags gives each kept value its slot -> write (all at once). Returns (kept, span)."""
    flags = [1 if v > threshold else 0 for v in values]           # one round
    slots, _, scan_rounds = prefix_sums_parallel(flags)          # log n rounds
    out = [None] * (slots[-1] if slots else 0)
    for i, v in enumerate(values):                               # one round: each writer has its own slot
        if flags[i]:
            out[slots[i] - 1] = v
    return out, scan_rounds + 2


def scan_in_place_bug(values: list) -> list:
    """The bug: each round updates the list in place, left to right, while still reading it."""
    a, step = list(values), 1
    while step < len(a):
        for i in range(step, len(a)):
            a[i] = a[i] + a[i - step]                            # a[i - step] may already hold this round's value
        step *= 2
    return a


if __name__ == "__main__":
    print([rounds_predicted(n) for n in (1, 2, 3, 16, 17, 1024)])
    print(parallel_filter([58, 25, 91, 12, 70, 47, 84, 31, 63], 50))
    print(scan_in_place_bug([3, 1, 4, 1, 5, 9, 2, 6]), prefix_sums_parallel([3, 1, 4, 1, 5, 9, 2, 6])[0])
