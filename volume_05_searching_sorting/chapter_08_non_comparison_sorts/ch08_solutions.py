"""Volume 5, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from ch08_examples import counting_sort, radix_sort


def sort_with_negatives(values: list[int]) -> list[int]:
    """Exercise 1: counting sort for a range lo..hi by shifting everything by -lo."""
    if not values:
        return []
    lo = min(values)
    return [v + lo for v in counting_sort([v - lo for v in values], max(values) - lo)]


def sort_grades(grades: list[str]) -> list[str]:
    """Exercise 2: letter grades A, B, C, D, F - five buckets."""
    order = "ABCDF"
    counts = {g: 0 for g in order}
    for g in grades:
        counts[g] += 1
    return [g for g in order for _ in range(counts[g])]


def maximum_gap(values: list[int]) -> int:
    """Exercise 3 (LeetCode 164): largest difference between neighbours in sorted order, via radix sort (linear)."""
    if len(values) < 2:
        return 0
    s = radix_sort(values)
    return max(b - a for a, b in zip(s, s[1:]))


def h_index_counting(citations: list[int]) -> int:
    """Exercise 4: h-index in O(n) - counts capped at n, then scan from the top (V5-C3 did it by sorting)."""
    n = len(citations)
    counts = [0] * (n + 1)
    for c in citations:
        counts[min(c, n)] += 1
    total = 0
    for h in range(n, -1, -1):
        total += counts[h]
        if total >= h:
            return h
    return 0


if __name__ == "__main__":
    print(sort_with_negatives([3, -2, 0, -5, 3]), sort_grades(list("CABFAB")), maximum_gap([3, 6, 9, 1]), h_index_counting([3, 0, 6, 1, 5]))
