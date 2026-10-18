"""Volume 10, Chapter 10 - Decrease-and-Conquer and Transform-and-Conquer.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import heapq


# ---------------------------------------------------------------- decrease by a constant
def insertion_sort(values: list[int]) -> list[int]:
    """Decrease by one: sort the first n - 1 items, then insert the last one into place (V5-C4)."""
    out = list(values)
    for i in range(1, len(out)):
        x, j = out[i], i - 1
        while j >= 0 and out[j] > x:
            out[j + 1] = out[j]
            j -= 1
        out[j + 1] = x
    return out


def josephus(n: int, k: int) -> int:
    """n people in a circle, every k-th leaves; who survives (0-based)? Decrease by one:
    after the first removal, it's the same puzzle with n - 1 people, renumbered. J(n) = (J(n-1) + k) mod n."""
    survivor = 0
    for size in range(2, n + 1):
        survivor = (survivor + k) % size
    return survivor


# ---------------------------------------------------------------- decrease by a constant factor
def find_fake_coin(weights: list[int]) -> tuple[int, int]:
    """One coin is lighter. Weigh thirds against each other: one weighing removes two thirds of the suspects.
    Returns (index of fake, weighings used) - about log base 3 of n."""
    lo, hi, weighings = 0, len(weights), 0
    while hi - lo > 1:
        third = (hi - lo + 2) // 3
        a, b = lo, lo + third
        left, right = sum(weights[a:a + third]), sum(weights[b:b + third])
        weighings += 1
        if left < right:
            lo, hi = a, a + third
        elif right < left:
            lo, hi = b, b + third
        else:
            lo = b + third
    return lo, weighings


# ---------------------------------------------------------------- decrease by a variable amount
def gcd(a: int, b: int) -> int:
    """Euclid: gcd(a, b) = gcd(b, a mod b). The problem shrinks by a varying amount each step (V2-C9)."""
    while b:
        a, b = b, a % b
    return a


# ---------------------------------------------------------------- transform: presorting
def has_duplicate_presort(values: list[int]) -> bool:
    """Instance simplification: after sorting, duplicates sit side by side. O(n log n) instead of O(n^2)."""
    s = sorted(values)
    return any(a == b for a, b in zip(s, s[1:]))


def mode_presort(values: list[int]) -> int:
    """The most common value: sort, then the longest run of equal neighbours."""
    s = sorted(values)
    best, best_len, run = s[0], 1, 1
    for a, b in zip(s, s[1:]):
        run = run + 1 if a == b else 1
        if run > best_len:
            best, best_len = b, run
    return best


# ---------------------------------------------------------------- transform: representation change
def horner(coefficients: list[int], x: int) -> int:
    """Evaluate c0 + c1 x + c2 x^2 + ... by rewriting as c0 + x(c1 + x(c2 + ...)): n multiplications, no powers."""
    result = 0
    for c in reversed(coefficients):
        result = result * x + c
    return result


def heap_sort(values: list[int]) -> list[int]:
    """Representation change: turn the list into a heap first (O(n)), then pop in order (V5-C7)."""
    heap = list(values)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


# ---------------------------------------------------------------- transform: problem reduction
def lcm(a: int, b: int) -> int:
    """Problem reduction: lcm is hard to search for directly, but lcm(a, b) = a * b / gcd(a, b)."""
    return a // gcd(a, b) * b


def bus_timetable_meeting(intervals: list[int]) -> int:
    """Industry example: buses leave every 12, 18, 30 minutes from the same depot - when do all leave together again?"""
    result = 1
    for t in intervals:
        result = lcm(result, t)
    return result


if __name__ == "__main__":
    print(insertion_sort([5, 2, 4, 6, 1, 3]), "| Josephus 7 people, every 3rd:", josephus(7, 3))
    coins = [10] * 27
    coins[19] = 9
    print("fake coin (index, weighings):", find_fake_coin(coins))
    print("gcd 1071, 462 =", gcd(1071, 462), "| lcm 4, 6 =", lcm(4, 6))
    print(has_duplicate_presort([3, 8, 1, 8]), mode_presort([4, 1, 4, 2, 1, 4]))
    print("2 + 3x + x^3 at x = 2:", horner([2, 3, 0, 1], 2), "|", heap_sort([9, 4, 7, 1, 8]))
    print("buses meet again after", bus_timetable_meeting([12, 18, 30]), "minutes")
