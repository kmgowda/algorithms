"""Chapter 11 - Binary Search: Halving Your Way to the Answer.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import bisect
from typing import Callable


def binary_search(sorted_items: list[str] | list[int], target: str | int) -> int:
    """Return the index of target in a SORTED list, or -1 if it is absent. O(log n).

    Loop invariant: if target is anywhere in the list, it is inside sorted_items[low..high].
    """
    low = 0
    high = len(sorted_items) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_items[middle] == target:
            return middle
        if sorted_items[middle] < target:
            low = middle + 1          # target can only be to the right
        else:
            high = middle - 1         # target can only be to the left
    return -1


def binary_search_trace(sorted_items: list[int], target: int) -> list[tuple[int, int, int]]:
    """Record (low, middle, high) at every step, to draw the search."""
    steps = []
    low, high = 0, len(sorted_items) - 1
    while low <= high:
        middle = (low + high) // 2
        steps.append((low, middle, high))
        if sorted_items[middle] == target:
            break
        if sorted_items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return steps


def comparisons_linear_vs_binary(n: int) -> tuple[int, int]:
    """Worst-case comparisons to search a sorted list of n numbers for a missing value."""
    items = list(range(n))
    target = n                       # not present: worst case for both
    linear = n
    binary = 0
    low, high = 0, n - 1
    while low <= high:
        binary += 1
        middle = (low + high) // 2
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return linear, binary


def first_at_or_after(sorted_times: list[int], wanted: int) -> int:
    """Lower bound: index of the first value >= wanted (len(list) if none).

    Practical example: the first bus that leaves at or after the time you arrive.
    """
    low, high = 0, len(sorted_times)    # note: high is one PAST the end
    while low < high:
        middle = (low + high) // 2
        if sorted_times[middle] < wanted:
            low = middle + 1
        else:
            high = middle
    return low


def next_bus(timetable: list[int], arrival: int) -> int | None:
    index = first_at_or_after(timetable, arrival)
    return timetable[index] if index < len(timetable) else None


def count_in_price_range(sorted_prices: list[float], low: float, high: float) -> int:
    """Industry example: a shop's price filter - how many products cost between low and high?"""
    left = bisect.bisect_left(sorted_prices, low)
    right = bisect.bisect_right(sorted_prices, high)
    return right - left


def first_bad_version(total_versions: int, is_bad: Callable[[int], bool]) -> int:
    """Industry example: find the first broken software release (versions 1..n).

    All versions before the first bad one are good; all after it are bad.
    """
    low, high = 1, total_versions
    while low < high:
        middle = (low + high) // 2
        if is_bad(middle):
            high = middle            # middle might be the first bad one
        else:
            low = middle + 1         # first bad one is after middle
    return low


def integer_square_root(n: int) -> int:
    """Binary search on the ANSWER: the largest whole number r with r * r <= n."""
    if n < 0:
        raise ValueError("no real square root for negative numbers")
    low, high = 0, n
    while low < high:
        middle = (low + high + 1) // 2   # round up so the range always shrinks
        if middle * middle <= n:
            low = middle
        else:
            high = middle - 1
    return low


def find_account(sorted_accounts: list[tuple[int, str]], account_number: int) -> str | None:
    """Industry example: accounts sorted by number; binary search on the first field."""
    numbers = [number for number, _ in sorted_accounts]   # in real systems this index is built once
    index = bisect.bisect_left(numbers, account_number)
    if index < len(numbers) and numbers[index] == account_number:
        return sorted_accounts[index][1]
    return None


if __name__ == "__main__":
    animals = ["ant", "bear", "cat", "deer", "eagle", "fox", "goat", "horse"]
    print("Index of fox:", binary_search(animals, "fox"))
    print("Trace for 70:", binary_search_trace([10, 20, 30, 40, 50, 60, 70, 80, 90], 70))
    for n in (100, 10_000, 1_000_000):
        linear, binary = comparisons_linear_vs_binary(n)
        print(f"n = {n:>9,}: linear search {linear:>9,} comparisons, binary search {binary} comparisons")
    timetable = [600, 630, 715, 800, 845, 930]
    print("Arrive 7:20 -> next bus:", next_bus(timetable, 720))
    prices = [99, 149, 199, 249, 299, 349, 499, 999]
    print("Products from 150 to 350:", count_in_price_range(prices, 150, 350))
    print("First bad version:", first_bad_version(100, lambda v: v >= 37))
    print("Integer square root of 1000:", integer_square_root(1000))
    print("Account 1042:", find_account([(1001, "Ana"), (1042, "Ben"), (1300, "Cy")], 1042))
