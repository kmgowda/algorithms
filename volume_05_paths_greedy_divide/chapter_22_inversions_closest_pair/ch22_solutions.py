"""Volume 5, Chapter 22 - Thinking Problems.

Problem 1: one swap of neighbours changes the inversion count by exactly one, so sorting by neighbour swaps needs
           exactly as many swaps as there are inversions (checked with insertion sort's swap count).
Problem 2: count pairs i < j with a[i] - a[j] > k in O(n log n), counting during merge sort.
Problem 3: merging with '<' instead of '<=' counts equal pairs as out of order.
"""

from __future__ import annotations


def neighbour_swaps(a: list) -> int:
    a, swaps = list(a), 0
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j - 1] > a[j]:
            a[j - 1], a[j] = a[j], a[j - 1]
            swaps += 1
            j -= 1
    return swaps


def gap_pairs(a: list, k) -> int:
    """Pairs i < j with a[i] > a[j] + k, counted between the halves of a merge sort before merging."""
    def go(v):
        if len(v) <= 1:
            return list(v), 0
        mid = len(v) // 2
        left, x = go(v[:mid])
        right, y = go(v[mid:])
        count, i = 0, 0
        for r in right:                                # left is sorted: skip the ones not big enough
            while i < len(left) and left[i] <= r + k:
                i += 1
            count += len(left) - i
        return sorted(left + right), x + y + count
    return go(a)[1]


def sort_count_strict(a: list) -> int:
    """The bug: take from the left only when strictly smaller."""
    if len(a) <= 1:
        return 0
    mid = len(a) // 2
    left, right = sorted(a[:mid]), sorted(a[mid:])
    i = j = cross = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            i += 1
        else:
            j += 1
            cross += len(left) - i
    return sort_count_strict(a[:mid]) + sort_count_strict(a[mid:]) + cross


if __name__ == "__main__":
    from ch22_examples import RANKS
    print(neighbour_swaps(RANKS), gap_pairs(RANKS, 2), sort_count_strict([2, 2]), sort_count_strict([3, 1, 3]))
