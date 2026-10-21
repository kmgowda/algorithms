"""Volume 3, Chapter 7 - Why Sorting Matters.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import random

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def is_sorted(a: list) -> bool:
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def inversions(a: list) -> list[tuple]:
    """Every pair that is out of order: a measure of how unsorted a list is (Figure 7.3)."""
    return [(a[i], a[j]) for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j]]


def has_duplicate_by_sorting(a: list) -> bool:
    """After sorting, equal values sit side by side: one pass finds them."""
    s = sorted(a)
    return any(s[i] == s[i + 1] for i in range(len(s) - 1))


def median(a: list):
    s = sorted(a)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def closest_pair(a: list) -> tuple:
    """The two closest values are neighbours once sorted."""
    s = sorted(a)
    return min(((s[i], s[i + 1]) for i in range(len(s) - 1)), key=lambda p: p[1] - p[0])


def group_counts(a: list) -> list[tuple]:
    """Runs of equal values after sorting: (value, count)."""
    out = []
    for v in sorted(a):
        if out and out[-1][0] == v:
            out[-1] = (v, out[-1][1] + 1)
        else:
            out.append((v, 1))
    return out


def overdue_pairs(days: list[int]) -> tuple[bool, tuple]:
    """Section 7.8: any equal pair, and the closest pair, by sorting then one pass."""
    return has_duplicate_by_sorting(days), closest_pair(days)


def stable_sort_demo() -> list[tuple]:
    loans = [("Ben", 3), ("Ana", 1), ("Cai", 3), ("Dev", 2), ("Eva", 1)]
    return sorted(loans, key=lambda r: r[1])


if __name__ == "__main__":
    inv = inversions(PILE)
    print(len(inv), inv[:6], 9 * 8 // 2)
    print(median(PILE), closest_pair(PILE), has_duplicate_by_sorting(PILE))
    print(group_counts([3, 1, 3, 2, 1, 3]), stable_sort_demo())
    rng = random.Random(1)
    a = [rng.randrange(1000) for _ in range(20)]
    print(len(inversions(sorted(a))), len(inversions(sorted(a, reverse=True))))
