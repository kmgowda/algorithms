"""Volume 5, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

import random

from ch06_examples import partition_lomuto


def partition_hoare(a: list, low: int, high: int) -> int:
    """Exercise 1: Hoare's original partition - two pointers walk inward and swap misplaced pairs.
    Returns j such that a[low..j] <= pivot <= a[j+1..high]."""
    pivot = a[(low + high) // 2]
    i, j = low - 1, high + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


def quicksort_hoare(a: list, low: int = 0, high: int | None = None) -> None:
    if high is None:
        high = len(a) - 1
    if low < high:
        p = partition_hoare(a, low, high)
        quicksort_hoare(a, low, p)
        quicksort_hoare(a, p + 1, high)


def partition_by_predicate(items: list, keep_left) -> int:
    """Exercise 2: move items where keep_left(x) is True to the front (e.g. in-stock products first).
    Returns how many are on the left. Order inside each side is not preserved."""
    boundary = 0
    for i in range(len(items)):
        if keep_left(items[i]):
            items[i], items[boundary] = items[boundary], items[i]
            boundary += 1
    return boundary


def median_of_three(a: list, low: int, high: int) -> int:
    """Exercise 3: index of the median of the first, middle, and last items - a cheap, sturdier pivot."""
    mid = (low + high) // 2
    trio = sorted([(a[low], low), (a[mid], mid), (a[high], high)])
    return trio[1][1]


def quicksort_median3(a: list, low: int = 0, high: int | None = None) -> None:
    if high is None:
        high = len(a) - 1
    if low < high:
        m = median_of_three(a, low, high)
        a[m], a[high] = a[high], a[m]
        p = partition_lomuto(a, low, high)
        quicksort_median3(a, low, p - 1)
        quicksort_median3(a, p + 1, high)


if __name__ == "__main__":
    a = [5, 1, 4, 2, 8, 2]
    quicksort_hoare(a)
    stock = ["milk:0", "eggs:5", "rice:0", "tea:3"]
    k = partition_by_predicate(stock, lambda s: not s.endswith(":0"))
    b = random.Random(1).sample(range(20), 20)
    quicksort_median3(b)
    print(a, stock[:k], b)
