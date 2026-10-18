"""Volume 7, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from math import gcd

from ch06_examples import LazySumTree, SegmentTree


class NumArray:
    """Exercise 1 (LeetCode 307): update one value, sum a range."""

    def __init__(self, nums: list[int]) -> None:
        self.tree = SegmentTree(nums)

    def update(self, index: int, val: int) -> None:
        self.tree.update(index, val)

    def sum_range(self, left: int, right: int) -> int:
        return int(self.tree.query(left, right))


def max_temperatures(readings: list[float], questions: list[tuple[int, int]]) -> list[float]:
    """Exercise 2: the hottest reading in each time range (a MAX segment tree)."""
    st = SegmentTree(readings, combine=max, identity=float("-inf"))
    return [st.query(a, b) for a, b in questions]


def corporate_bookings(bookings: list[tuple[int, int, int]], n: int) -> list[int]:
    """Exercise 3 (LeetCode 1109): add seats to flight ranges, then read each flight's total."""
    t = LazySumTree([0] * n)
    for first, last, seats in bookings:
        t.add(first - 1, last - 1, seats)
    return [t.total(i, i) for i in range(n)]


def gcd_ranges(values: list[int], questions: list[tuple[int, int]]) -> list[int]:
    """Exercise 4: any associative operation works - here the greatest common divisor (identity 0)."""
    st = SegmentTree(values, combine=gcd, identity=0)
    return [int(st.query(a, b)) for a, b in questions]


if __name__ == "__main__":
    na = NumArray([1, 3, 5])
    print(na.sum_range(0, 2), end=" ")
    na.update(1, 2)
    print(na.sum_range(0, 2), max_temperatures([21, 25, 19, 30, 22], [(0, 2), (1, 4)]),
          corporate_bookings([(1, 2, 10), (2, 3, 20), (2, 5, 25)], 5), gcd_ranges([12, 18, 24, 7], [(0, 2), (0, 3)]))
