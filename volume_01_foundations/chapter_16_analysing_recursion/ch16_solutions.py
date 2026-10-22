"""Volume 1, Chapter 16, Thinking Problem 2: the shortest and the tallest child together, by halves.

min_max splits the line in two, finds the shortest and tallest of each half recursively, and compares the two
shortest and the two tallest: C(1) = 0, C(2) = 1, C(n) = 2C(n/2) + 2, which is 3n/2 - 2 when n is a power of two.
"""
from __future__ import annotations


def min_max(heights: list[int], low: int, high: int) -> tuple[int, int, int]:
    """Smallest and largest of heights[low..high], and the comparisons used."""
    if low == high:
        return heights[low], heights[low], 0
    if high == low + 1:
        if heights[low] < heights[high]:
            return heights[low], heights[high], 1
        return heights[high], heights[low], 1
    mid = (low + high) // 2
    s1, t1, c1 = min_max(heights, low, mid)
    s2, t2, c2 = min_max(heights, mid + 1, high)
    return min(s1, s2), max(t1, t2), c1 + c2 + 2


def shortest_and_tallest(heights: list[int]) -> tuple[int, int, int]:
    """min_max over the whole line; an empty line has no shortest or tallest child."""
    if not heights:
        raise ValueError("an empty line has no shortest or tallest child")
    return min_max(heights, 0, len(heights) - 1)


if __name__ == "__main__":
    print(shortest_and_tallest([142, 155, 138, 161, 150, 158]))
