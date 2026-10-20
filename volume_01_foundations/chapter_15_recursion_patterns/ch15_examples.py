"""Volume 1, Chapter 15 - Recursion Patterns.

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def power(x: int, n: int) -> int:
    """x to the n (n >= 0) by halving the exponent: O(log n) multiplications (Figure 15.1)."""
    if n == 0:
        return 1
    half = power(x, n // 2)
    return half * half if n % 2 == 0 else x * half * half


def permutations(items: list[str]) -> list[list[str]]:
    """Every arrangement: choose each item first, then arrange the rest (Figure 15.2)."""
    if not items:
        return [[]]
    result = []
    for i, x in enumerate(items):
        for p in permutations(items[:i] + items[i + 1:]):
            result.append([x] + p)
    return result


def subsets(items: list[str]) -> list[list[str]]:
    """Every subset of items: decide the first item in or out, then recurse on the rest (Figure 15.3)."""
    if not items:
        return [[]]
    rest = subsets(items[1:])
    return [[items[0]] + s for s in rest] + rest


def search(shelf: list[int], target: int, low: int, high: int) -> int:
    """Recursive binary search on positions low..high, never copying the shelf (Figure 15.4); -1 if absent."""
    if low > high:
        return -1
    mid = (low + high) // 2
    if shelf[mid] == target:
        return mid
    if shelf[mid] < target:
        return search(shelf, target, mid + 1, high)
    return search(shelf, target, low, mid - 1)


if __name__ == "__main__":
    print(power(3, 13), power(2, 10))
    print(["".join(p) for p in permutations(list("ABC"))])
    print(["".join(s) or "{}" for s in subsets(list("ABC"))])
    print(search(SHELF, 63, 0, len(SHELF) - 1), search(SHELF, 50, 0, len(SHELF) - 1))
