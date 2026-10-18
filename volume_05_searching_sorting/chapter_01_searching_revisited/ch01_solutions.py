"""Volume 5, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from ch01_examples import first_true


def binary_search_recursive(items: list, target, low: int = 0, high: int | None = None) -> int:
    """Exercise 1: the same search written recursively (V2-C7). O(log n) time and stack."""
    if high is None:
        high = len(items) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if items[mid] == target:
        return mid
    if items[mid] < target:
        return binary_search_recursive(items, target, mid + 1, high)
    return binary_search_recursive(items, target, low, mid - 1)


def min_ship_capacity(parcels: list[int], days: int) -> int:
    """Exercise 2 (LeetCode 1011): smallest truck capacity that ships parcels (in order) within `days`."""
    def ok(cap: int) -> bool:
        used, load = 1, 0
        for p in parcels:
            if load + p > cap:
                used, load = used + 1, 0
            load += p
        return used <= days
    return first_true(max(parcels), sum(parcels), ok)


def earliest_bloom_day(bloom: list[int], bouquets: int, size: int) -> int:
    """Exercise 3 (LeetCode 1482): earliest day to make `bouquets` bouquets of `size` adjacent flowers. -1 if impossible."""
    if bouquets * size > len(bloom):
        return -1

    def ok(day: int) -> bool:
        made = run = 0
        for b in bloom:
            run = run + 1 if b <= day else 0
            if run == size:
                made, run = made + 1, 0
        return made >= bouquets
    return first_true(min(bloom), max(bloom), ok)


def cube_root_floor(n: int) -> int:
    """Exercise 4: largest r with r^3 <= n."""
    return first_true(0, max(1, n), lambda r: (r + 1) ** 3 > n)


if __name__ == "__main__":
    print(binary_search_recursive([1, 3, 5, 7], 7), min_ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))
    print(earliest_bloom_day([1, 10, 3, 10, 2], 3, 1), cube_root_floor(30))
