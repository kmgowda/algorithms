"""Volume 5, Chapter 6 - Quicksort: Partitioning Around a Pivot; Randomization.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import random
import sys


def partition_lomuto(a: list, low: int, high: int) -> int:
    """Use a[high] as the pivot. Everything < pivot ends up left of it. Returns the pivot's final index."""
    pivot = a[high]
    boundary = low                       # a[low:boundary] holds items smaller than the pivot
    for i in range(low, high):
        if a[i] < pivot:
            a[i], a[boundary] = a[boundary], a[i]
            boundary += 1
    a[boundary], a[high] = a[high], a[boundary]
    return boundary


def quicksort(a: list, low: int = 0, high: int | None = None, rng: random.Random | None = None) -> None:
    """In-place quicksort with a RANDOM pivot: expected O(n log n) on every input."""
    if high is None:
        high = len(a) - 1
    rng = rng or random
    while low < high:
        r = rng.randint(low, high)
        a[r], a[high] = a[high], a[r]    # move the random pivot to the end
        p = partition_lomuto(a, low, high)
        if p - low < high - p:           # recurse on the smaller side, loop on the larger: O(log n) stack
            quicksort(a, low, p - 1, rng)
            low = p + 1
        else:
            quicksort(a, p + 1, high, rng)
            high = p - 1


def quicksort_first_pivot_comparisons(items: list) -> int:
    """Naive quicksort (always the FIRST item as pivot), counting comparisons - to show the worst case."""
    comparisons = 0
    stack = [list(items)]
    while stack:
        part = stack.pop()
        if len(part) <= 1:
            continue
        pivot, rest = part[0], part[1:]
        comparisons += len(rest)
        stack.append([x for x in rest if x < pivot])
        stack.append([x for x in rest if x >= pivot])
    return comparisons


def partition_three_way(a: list, low: int, high: int) -> tuple[int, int]:
    """Dutch-flag partition (V4-C5): < pivot | == pivot | > pivot. Returns the bounds of the middle block."""
    pivot = a[low]
    lt, i, gt = low, low, high
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def quicksort_three_way(a: list, low: int = 0, high: int | None = None, rng: random.Random | None = None) -> None:
    """Great when there are many duplicates (exam grades, star ratings): equal items are finished in one go."""
    if high is None:
        high = len(a) - 1
    if low >= high:
        return
    rng = rng or random
    r = rng.randint(low, high)
    a[low], a[r] = a[r], a[low]
    lt, gt = partition_three_way(a, low, high)
    quicksort_three_way(a, low, lt - 1, rng)
    quicksort_three_way(a, gt + 1, high, rng)


def sort_star_ratings(ratings: list[int]) -> list[int]:
    """Industry example: millions of 1-5 star ratings - three-way quicksort handles the huge number of ties."""
    a = list(ratings)
    quicksort_three_way(a, rng=random.Random(0))
    return a


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    cards = [7, 2, 9, 4, 3, 8, 5]
    print("after one partition:", (lambda a: (partition_lomuto(a, 0, len(a) - 1), a))(list(cards)))
    q = list(cards)
    quicksort(q, rng=random.Random(1))
    print("quicksort:", q)
    print("first-pivot comparisons, random vs sorted (n=300):",
          quicksort_first_pivot_comparisons(random.Random(2).sample(range(300), 300)),
          quicksort_first_pivot_comparisons(list(range(300))))
    print(sort_star_ratings([5, 3, 5, 1, 4, 5, 2, 5, 3, 4]))
