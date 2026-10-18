"""Volume 4, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def contains_nearby_duplicate(ids: list[int], k: int) -> bool:
    """Exercise 1 (LeetCode 219): the same id twice within k positions? Store each id's last index."""
    last: dict[int, int] = {}
    for i, x in enumerate(ids):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False


def subarray_sum_divisible(values: list[int], k: int) -> int:
    """Exercise 2 (LeetCode 974): count runs whose sum is divisible by k (equal prefix remainders)."""
    counts = {0: 1}
    running = total = 0
    for v in values:
        running = (running + v) % k
        total += counts.get(running, 0)
        counts[running] = counts.get(running, 0) + 1
    return total


def isomorphic(a: str, b: str) -> bool:
    """Exercise 3 (LeetCode 205): can letters of a be renamed one-to-one to get b?"""
    if len(a) != len(b):
        return False
    forward: dict[str, str] = {}
    backward: dict[str, str] = {}
    for x, y in zip(a, b):
        if forward.setdefault(x, y) != y or backward.setdefault(y, x) != x:
            return False
    return True


def four_sum_count(a: list[int], b: list[int], c: list[int], d: list[int]) -> int:
    """Exercise 4 (LeetCode 454): meet in the middle - count a+b sums, then look up -(c+d)."""
    ab: dict[int, int] = {}
    for x in a:
        for y in b:
            ab[x + y] = ab.get(x + y, 0) + 1
    return sum(ab.get(-(x + y), 0) for x in c for y in d)


if __name__ == "__main__":
    print(contains_nearby_duplicate([1, 2, 3, 1], 3), subarray_sum_divisible([4, 5, 0, -2, -3, 1], 5))
    print(isomorphic("egg", "add"), isomorphic("foo", "bar"), four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2]))
