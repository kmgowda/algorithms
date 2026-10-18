"""Volume 10, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations


def boyer_moore_majority(values: list[int]) -> int | None:
    """Exercise 1: majority in O(n) time and O(1) space - pair off different values; survivors are candidates."""
    candidate, count = None, 0
    for v in values:
        if count == 0:
            candidate = v
        count += 1 if v == candidate else -1
    return candidate if values and values.count(candidate) * 2 > len(values) else None


def kth_smallest_two_sorted(a: list[int], b: list[int], k: int) -> int:
    """Exercise 2: k-th smallest (1-based) of two sorted lists - discard k/2 items from one list each step. O(log k)."""
    while True:
        if not a:
            return b[k - 1]
        if not b:
            return a[k - 1]
        if k == 1:
            return min(a[0], b[0])
        i = min(len(a), k // 2)
        j = min(len(b), k // 2)
        if a[i - 1] <= b[j - 1]:
            a, k = a[i:], k - i
        else:
            b, k = b[j:], k - j


def peak_index(values: list[int]) -> int:
    """Exercise 3 (LeetCode 162): any element bigger than its neighbours - go toward the higher side. O(log n)."""
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < values[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def reverse_pairs(values: list[int]) -> int:
    """Exercise 4 (LeetCode 493): pairs i < j with values[i] > 2 * values[j] - inversion counting with a twist."""
    def solve(v: list[int]) -> tuple[int, list[int]]:
        if len(v) <= 1:
            return 0, v
        mid = len(v) // 2
        cl, left = solve(v[:mid])
        cr, right = solve(v[mid:])
        count, j = cl + cr, 0
        for x in left:
            while j < len(right) and x > 2 * right[j]:
                j += 1
            count += j
        return count, sorted(left + right)
    return solve(list(values))[0]


if __name__ == "__main__":
    print(boyer_moore_majority([3, 3, 4, 2, 3, 3, 1]), kth_smallest_two_sorted([1, 3, 8], [2, 4, 9, 10], 4),
          peak_index([1, 3, 5, 4, 2]), reverse_pairs([1, 3, 2, 3, 1]))
