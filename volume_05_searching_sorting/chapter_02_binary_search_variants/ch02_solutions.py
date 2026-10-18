"""Volume 5, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from ch02_examples import lower_bound, upper_bound


def insert_position(items: list[int], target: int) -> int:
    """Exercise 1 (LeetCode 35): where target is, or where it would be inserted."""
    return lower_bound(items, target)


def next_letter(letters: list[str], target: str) -> str:
    """Exercise 2 (LeetCode 744): smallest letter strictly greater than target, wrapping around."""
    i = upper_bound(letters, target)
    return letters[i % len(letters)]


def mountain_top(heights: list[int]) -> int:
    """Exercise 3 (LeetCode 852): heights strictly rise then strictly fall. Index of the top."""
    low, high = 0, len(heights) - 1
    while low < high:
        mid = (low + high) // 2
        if heights[mid] < heights[mid + 1]:
            low = mid + 1
        else:
            high = mid
    return low


def k_closest(items: list[int], k: int, x: int) -> list[int]:
    """Exercise 4 (LeetCode 658): the k items closest to x (ties prefer smaller), in sorted order.
    Binary search the LEFT edge of the window of k."""
    low, high = 0, len(items) - k
    while low < high:
        mid = (low + high) // 2
        if x - items[mid] > items[mid + k] - x:
            low = mid + 1
        else:
            high = mid
    return items[low:low + k]


def kth_missing(items: list[int], k: int) -> int:
    """Exercise 5 (LeetCode 1539): sorted positive numbers; the k-th positive integer not in the list.
    Before index i, items[i] - (i + 1) numbers are missing."""
    low, high = 0, len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] - (mid + 1) < k:
            low = mid + 1
        else:
            high = mid
    return low + k


if __name__ == "__main__":
    print(insert_position([1, 3, 5, 6], 4), next_letter(["c", "f", "j"], "j"), mountain_top([0, 2, 5, 3, 1]))
    print(k_closest([1, 2, 3, 4, 5], 4, 3), kth_missing([2, 3, 4, 7, 11], 5))
