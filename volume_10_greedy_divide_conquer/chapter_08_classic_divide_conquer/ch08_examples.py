"""Volume 10, Chapter 8 - Classic Divide and Conquer: Max/Min, Inversions, Closest Pair, Majority.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import math


def max_min(values: list[int], lo: int = 0, hi: int | None = None) -> tuple[int, int, int]:
    """Largest and smallest together. Returns (max, min, comparisons). About 3n/2 comparisons instead of 2n:
    the two halves' answers combine with just 2 comparisons, and pairs cost only 1."""
    hi = len(values) - 1 if hi is None else hi
    if lo == hi:
        return values[lo], values[lo], 0
    if hi == lo + 1:
        a, b = values[lo], values[hi]
        return (a, b, 1) if a > b else (b, a, 1)
    mid = (lo + hi) // 2
    mx1, mn1, c1 = max_min(values, lo, mid)
    mx2, mn2, c2 = max_min(values, mid + 1, hi)
    return max(mx1, mx2), min(mn1, mn2), c1 + c2 + 2


def count_inversions(values: list[int]) -> tuple[int, list[int]]:
    """Pairs (i < j) with values[i] > values[j] - how 'unsorted' a list is. Merge sort that counts:
    when an item from the right half jumps ahead, it passes every item still waiting in the left half. O(n log n)."""
    if len(values) <= 1:
        return 0, list(values)
    mid = len(values) // 2
    left_inv, left = count_inversions(values[:mid])
    right_inv, right = count_inversions(values[mid:])
    merged, i, j, cross = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            cross += len(left) - i
            j += 1
    merged += left[i:] + right[j:]
    return left_inv + right_inv + cross, merged


Point = tuple[float, float]


def closest_pair(points: list[Point]) -> float:
    """Smallest distance between any two points in O(n log n). Split by x; the answer is in the left, the right,
    or a narrow strip around the dividing line - where each point need only check a few neighbours sorted by y."""
    px = sorted(points)

    def solve(pts: list[Point]) -> tuple[float, list[Point]]:
        n = len(pts)
        if n <= 3:
            best = min((math.dist(a, b) for i, a in enumerate(pts) for b in pts[i + 1:]), default=math.inf)
            return best, sorted(pts, key=lambda p: p[1])
        mid = n // 2
        mid_x = pts[mid][0]
        dl, left_y = solve(pts[:mid])
        dr, right_y = solve(pts[mid:])
        d = min(dl, dr)
        by_y = sorted(left_y + right_y, key=lambda p: p[1])     # (a linear merge keeps it O(n log n); sorting is simpler)
        strip = [p for p in by_y if abs(p[0] - mid_x) < d]
        for i, p in enumerate(strip):
            for q in strip[i + 1:i + 8]:                         # at most 7 later points can be closer than d
                if q[1] - p[1] >= d:
                    break
                d = min(d, math.dist(p, q))
        return d, by_y

    return solve(px)[0]


def closest_pair_brute(points: list[Point]) -> float:
    return min((math.dist(a, b) for i, a in enumerate(points) for b in points[i + 1:]), default=math.inf)


def majority(values: list[int]) -> int | None:
    """A value appearing in more than half the list. Divide and conquer: a majority of the whole must be a
    majority of at least one half - check the two candidates. O(n log n)."""
    def solve(lo: int, hi: int) -> int | None:
        if lo == hi:
            return values[lo]
        mid = (lo + hi) // 2
        candidates = {solve(lo, mid), solve(mid + 1, hi)} - {None}
        for c in candidates:
            if sum(1 for k in range(lo, hi + 1) if values[k] == c) * 2 > hi - lo + 1:
                return c
        return None
    return solve(0, len(values) - 1) if values else None


def ranking_disagreement(ranking_a: list[str], ranking_b: list[str]) -> int:
    """Industry example: how different are two people's rankings? Count inversions (used in recommendation systems)."""
    position = {item: i for i, item in enumerate(ranking_a)}
    return count_inversions([position[item] for item in ranking_b])[0]


if __name__ == "__main__":
    temps = [31, 28, 35, 22, 40, 19, 33, 27]
    print("hottest, coldest, comparisons:", max_min(temps))
    print("inversions:", count_inversions([2, 4, 1, 3, 5])[0])
    print("ranking disagreement:", ranking_disagreement(["Jaws", "Up", "Cars", "Coco"], ["Up", "Coco", "Jaws", "Cars"]))
    towers = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("closest towers:", round(closest_pair(towers), 3), round(closest_pair_brute(towers), 3))
    print("majority vote:", majority([3, 3, 4, 2, 3, 3, 1]), majority([1, 2, 3]))
