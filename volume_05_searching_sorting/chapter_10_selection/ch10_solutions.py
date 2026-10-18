"""Volume 5, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

import heapq
import random

from ch10_examples import quickselect


def kth_largest(values: list[int], k: int) -> int:
    """Exercise 1 (LeetCode 215): the k-th largest is the (n - k + 1)-th smallest."""
    return quickselect(values, len(values) - k + 1, random.Random(0))


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """Exercise 2 (LeetCode 347 idea): k most frequent words; ties alphabetical. Count, then select."""
    counts: dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return [w for w, _ in heapq.nsmallest(k, counts.items(), key=lambda item: (-item[1], item[0]))]


def best_meeting_point(houses: list[int]) -> int:
    """Exercise 3: the point on a street minimizing total walking distance is a MEDIAN of the house positions."""
    return quickselect(houses, (len(houses) + 1) // 2, random.Random(0))


def wiggle_sort(values: list[int]) -> list[int]:
    """Exercise 4 (LeetCode 280 idea): small, big, small, big... (a[0] <= a[1] >= a[2] <= a[3] ...)."""
    a = list(values)
    for i in range(1, len(a)):
        if (i % 2 == 1 and a[i] < a[i - 1]) or (i % 2 == 0 and a[i] > a[i - 1]):
            a[i], a[i - 1] = a[i - 1], a[i]
    return a


if __name__ == "__main__":
    print(kth_largest([3, 2, 1, 5, 6, 4], 2), top_k_frequent("the lion and the zebra and the bird".split(), 2))
    print(best_meeting_point([1, 7, 3, 9, 2]), wiggle_sort([3, 5, 2, 1, 6, 4]))
