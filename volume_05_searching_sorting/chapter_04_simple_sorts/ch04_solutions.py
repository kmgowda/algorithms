"""Volume 5, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from ch04_examples import insertion_sort


def count_inversions_slow(items: list) -> int:
    """Exercise 1: pairs (i < j) with items[i] > items[j]. Insertion sort's shift count equals this number."""
    return sum(1 for i in range(len(items)) for j in range(i + 1, len(items)) if items[i] > items[j])


def insertion_sort_desc(items: list) -> list:
    """Exercise 2: largest first - flip one comparison."""
    a = list(items)
    for i in range(1, len(a)):
        card, j = a[i], i - 1
        while j >= 0 and a[j] < card:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = card
    return a


def sort_k_sorted(items: list, k: int) -> list:
    """Exercise 3: every item is at most k places from its sorted position. Insertion sort takes O(n*k)."""
    return insertion_sort(items)[0]


def bubble_passes(items: list) -> int:
    """Exercise 4: how many full passes does early-exit bubble sort make? (including the final check pass)"""
    a = list(items)
    passes = 0
    for end in range(len(a) - 1, 0, -1):
        passes += 1
        swapped = False
        for i in range(end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
    return passes


if __name__ == "__main__":
    print(count_inversions_slow([3, 1, 2]), insertion_sort_desc([3, 1, 2]), sort_k_sorted([2, 1, 4, 3, 6, 5], 1))
    print(bubble_passes([1, 2, 3, 4]), bubble_passes([4, 3, 2, 1]))
