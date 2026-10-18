"""Volume 4, Chapter 5 - Two Pointers: Walking From Both Ends, or Reading and Writing.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations


def pair_with_sum_sorted(prices: list[int], budget: int) -> tuple[int, int] | None:
    """Opposite ends (LeetCode 167): sorted prices; move the pointer that fixes the sum. O(n), O(1) space."""
    left, right = 0, len(prices) - 1
    while left < right:
        total = prices[left] + prices[right]
        if total == budget:
            return left, right
        if total < budget:
            left += 1            # need more: the smallest item can't be part of any answer
        else:
            right -= 1           # need less: the largest item can't be part of any answer
    return None


def three_sum_zero(values: list[int]) -> list[tuple[int, int, int]]:
    """LeetCode 15: all unique triples adding to 0. Sort, fix one, two-pointer the rest. O(n^2)."""
    values = sorted(values)
    out: list[tuple[int, int, int]] = []
    for i in range(len(values) - 2):
        if i and values[i] == values[i - 1]:
            continue
        left, right = i + 1, len(values) - 1
        while left < right:
            s = values[i] + values[left] + values[right]
            if s == 0:
                out.append((values[i], values[left], values[right]))
                left += 1
                while left < right and values[left] == values[left - 1]:
                    left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return out


def max_water(heights: list[int]) -> int:
    """LeetCode 11: two walls hold water = shorter wall x distance. Move the shorter wall inward."""
    left, right, best = 0, len(heights) - 1, 0
    while left < right:
        best = max(best, min(heights[left], heights[right]) * (right - left))
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best


def compact_valid_readings(readings: list[int], minimum: int) -> int:
    """Read/write pointers (LeetCode 27 idea): keep readings >= minimum at the front, in order. Returns count."""
    write = 0
    for read in range(len(readings)):
        if readings[read] >= minimum:
            readings[write] = readings[read]
            write += 1
    return write


def merge_sorted_schedules(a: list[int], b: list[int]) -> list[int]:
    """Two lists, one pointer each (V1-C12): merge two sorted bus timetables."""
    i = j = 0
    out: list[int] = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]


def is_subsequence(pattern: str, text: str) -> bool:
    """LeetCode 392: are pattern's letters found in text, in order (not necessarily together)?"""
    i = 0
    for ch in text:
        if i < len(pattern) and pattern[i] == ch:
            i += 1
    return i == len(pattern)


def boats_needed(weights: list[int], limit: int) -> int:
    """Industry example (LeetCode 881): rescue boats carry at most 2 people under a weight limit.

    Pair the heaviest with the lightest when possible.
    """
    weights = sorted(weights)
    light, heavy, boats = 0, len(weights) - 1, 0
    while light <= heavy:
        if weights[light] + weights[heavy] <= limit:
            light += 1
        heavy -= 1
        boats += 1
    return boats


if __name__ == "__main__":
    print(pair_with_sum_sorted([150, 300, 450, 700], 750), three_sum_zero([-1, 0, 1, 2, -1, -4]))
    print(max_water([1, 8, 6, 2, 5, 4, 8, 3, 7]))
    r = [12, 3, 25, 8, 30]
    n = compact_valid_readings(r, 10)
    print(r[:n], merge_sorted_schedules([600, 715, 900], [630, 800]))
    print(is_subsequence("zoo", "zebra on tour"), boats_needed([3, 2, 2, 1], 3))
