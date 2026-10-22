"""Volume 4, Chapter 6 - Thinking Problems (Section 6.15): model solutions.

Run:  python3 ch06_solutions.py
"""

from __future__ import annotations

import ch06_examples as ex


def refresh_catalogue(cat: list, new: list) -> tuple[list, int]:
    """Thinking Problem 2: insertion-sort the k new entries alone, then merge them into the sorted
    catalogue. At most k(k - 1)/2 + n + k - 1 comparisons, wherever the new entries belong."""
    extra = list(new)
    comparisons = ex.insertion_sort(extra)["comparisons"]
    out, i, j = [], 0, 0
    while i < len(cat) and j < len(extra):
        comparisons += 1
        if cat[i] <= extra[j]:              # an old entry stays ahead of an equal new one
            out.append(cat[i])
            i += 1
        else:
            out.append(extra[j])
            j += 1
    out.extend(cat[i:])
    out.extend(extra[j:])
    return out, comparisons


def binary_insertion_sort(a: list, key=lambda v: v) -> int:
    """Thinking Problem 3, corrected: binary search for the first item LARGER than x, so the sort stays
    stable. Returns the number of comparisons."""
    comparisons = 0
    for i in range(1, len(a)):
        x = a[i]
        lo, hi = 0, i
        while lo < hi:
            mid = (lo + hi) // 2
            comparisons += 1
            if key(a[mid]) > key(x):
                hi = mid
            else:
                lo = mid + 1
        a[lo + 1:i + 1] = a[lo:i]
        a[lo] = x
    return comparisons


if __name__ == "__main__":
    import random
    rng = random.Random(1)
    cat = sorted(rng.sample(range(200_000), 20_000))
    print(refresh_catalogue(cat, [rng.randrange(200_000) for _ in range(50)])[1])
    print(binary_insertion_sort([rng.random() for _ in range(1000)]))
