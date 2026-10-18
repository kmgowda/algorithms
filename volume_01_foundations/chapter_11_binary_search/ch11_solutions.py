"""Chapter 11 - Solutions to the exercises."""

from __future__ import annotations


def max_guesses(n: int) -> int:
    """Exercise 2: worst-case guesses for the 1..n guessing game = number of bits in n."""
    return n.bit_length()


def binary_search_recursive(items: list[int], target: int, low: int = 0, high: int | None = None) -> int:
    """Exercise 4 (preview of recursion): the same search, where the function calls itself."""
    if high is None:
        high = len(items) - 1
    if low > high:
        return -1
    middle = (low + high) // 2
    if items[middle] == target:
        return middle
    if items[middle] < target:
        return binary_search_recursive(items, target, middle + 1, high)
    return binary_search_recursive(items, target, low, middle - 1)


def first_occurrence(items: list[int], target: int) -> int:
    """Exercise 5: leftmost index of target in a sorted list with duplicates, or -1."""
    low, high = 0, len(items)
    while low < high:
        middle = (low + high) // 2
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low if low < len(items) and items[low] == target else -1


def search_insert_position(items: list[int], target: int) -> int:
    """Exercise 6 (LeetCode 35): where target is, or where it would be inserted."""
    low, high = 0, len(items)
    while low < high:
        middle = (low + high) // 2
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low


def min_daily_capacity(parcels: list[int], days: int) -> int:
    """Exercise 7 (binary search on the answer): smallest truck capacity that ships
    all parcels, in order, within `days` days (LeetCode 1011, in delivery-company clothes)."""
    def days_needed(capacity: int) -> int:
        used_days, load = 1, 0
        for parcel in parcels:
            if load + parcel > capacity:
                used_days += 1
                load = 0
            load += parcel
        return used_days

    low, high = max(parcels), sum(parcels)
    while low < high:
        middle = (low + high) // 2
        if days_needed(middle) <= days:
            high = middle
        else:
            low = middle + 1
    return low


if __name__ == "__main__":
    print(max_guesses(100), max_guesses(1_000_000))
    print(binary_search_recursive([2, 4, 6, 8], 6), first_occurrence([1, 2, 2, 2, 3], 2))
    print(search_insert_position([1, 3, 5, 6], 4), min_daily_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))
