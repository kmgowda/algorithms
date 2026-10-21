"""Volume 4, Chapter 20 - Counting Inversions and Closest Pairs: two divide-and-conquer classics.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

import math

# Two readers ranked the same eight books; positions in reader B's list, in reader A's order.
RANKS = [3, 1, 4, 8, 2, 6, 7, 5]
# Book-drop boxes around town (x, y) in hundreds of metres.
BOXES = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), (20, 25), (35, 8)]


def inversions_brute(a: list) -> int:
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def sort_count(a: list) -> tuple[list, int]:
    """Merge sort that also counts pairs out of order (Figure 20.2)."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, x = sort_count(a[:mid])
    right, y = sort_count(a[mid:])
    out, i, j, cross = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
            cross += len(left) - i                    # right[j] jumps ahead of every item left in the left half
    return out + left[i:] + right[j:], x + y + cross


def closest_brute(pts: list) -> tuple[float, tuple]:
    best = (math.inf, None)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            best = min(best, (math.dist(pts[i], pts[j]), (pts[i], pts[j])))
    return best


def closest_pair(pts: list) -> tuple[float, tuple]:
    """Divide by x, solve both halves, then check only a narrow strip around the dividing line (Figure 20.4)."""
    def solve(p):
        if len(p) <= 3:
            return closest_brute(p)
        mid = len(p) // 2
        x_mid = p[mid][0]
        best = min(solve(p[:mid]), solve(p[mid:]))
        strip = sorted((q for q in p if abs(q[0] - x_mid) < best[0]), key=lambda q: q[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= best[0]:
                    break
                best = min(best, (math.dist(strip[i], strip[j]), (strip[i], strip[j])))
        return best
    return solve(sorted(pts))


if __name__ == "__main__":
    print(inversions_brute(RANKS), sort_count(RANKS))
    print(closest_brute(BOXES), closest_pair(BOXES))
