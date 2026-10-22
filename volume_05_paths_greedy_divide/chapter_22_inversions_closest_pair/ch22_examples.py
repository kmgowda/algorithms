"""Volume 5, Chapter 20 - Counting Inversions and Closest Pairs: two divide-and-conquer classics.

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


def closest_pair(pts: list, counter: list | None = None) -> tuple[float, tuple]:
    """Divide by x, solve both halves, then check only a narrow strip around the dividing line (Figures 20.3 and 20.4).
    The points are sorted by x and by y once, at the start; every call splits its y-sorted list in two in linear
    time, so no call sorts again and the whole method is O(n log n). counter[0] counts distance calculations."""
    counter = counter if counter is not None else [0]

    def dist(p, q):
        counter[0] += 1
        return math.dist(p[:2], q[:2])

    def solve(px, py):
        if len(px) <= 3:
            best = (math.inf, None)
            for i in range(len(px)):
                for j in range(i + 1, len(px)):
                    best = min(best, (dist(px[i], px[j]), (px[i], px[j])))
            return best
        mid = len(px) // 2
        x_mid = px[mid][0]
        left_tags = {q[2] for q in px[:mid]}
        py_left = [q for q in py if q[2] in left_tags]           # the y order survives the split
        py_right = [q for q in py if q[2] not in left_tags]
        best = min(solve(px[:mid], py_left), solve(px[mid:], py_right))
        strip = [q for q in py if abs(q[0] - x_mid) < best[0]]   # already in y order: no sorting here
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):        # at most 7 later points can be close enough
                if strip[j][1] - strip[i][1] >= best[0]:
                    break
                best = min(best, (dist(strip[i], strip[j]), (strip[i], strip[j])))
        return best

    tagged = [(x, y, k) for k, (x, y) in enumerate(pts)]          # the tag k keeps repeated points apart
    d, pair = solve(sorted(tagged), sorted(tagged, key=lambda q: (q[1], q[0], q[2])))
    if pair is None:
        return d, None
    a, b = sorted((pair[0][:2], pair[1][:2]))
    return d, (a, b)


def closest_pair_resorting(pts: list) -> float:
    """The simpler version that sorts each strip by y inside every call: O(n log^2 n) (Chapter 19, Figure 19.4)."""
    def solve(p):
        if len(p) <= 3:
            return closest_brute(p)[0]
        mid = len(p) // 2
        x_mid = p[mid][0]
        best = min(solve(p[:mid]), solve(p[mid:]))
        strip = sorted((q for q in p if abs(q[0] - x_mid) < best), key=lambda q: q[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= best:
                    break
                best = min(best, math.dist(strip[i], strip[j]))
        return best
    return solve(sorted(pts))


def strip_candidates(pts: list, x_mid: float, d: float) -> int:
    """The largest number of later strip points any point is compared with (at most 7, Figure 20.4)."""
    strip = sorted((q for q in pts if abs(q[0] - x_mid) < d), key=lambda q: q[1])
    most = 0
    for i in range(len(strip)):
        k = 0
        for j in range(i + 1, len(strip)):
            if strip[j][1] - strip[i][1] >= d:
                break
            k += 1
        most = max(most, k)
    return most


def kendall_tau(a: list) -> float:
    """Section 20.7: 1 - 2 x (share of pairs in opposite order)."""
    n = len(a)
    return 1 - 2 * sort_count(a)[1] / (n * (n - 1) / 2)


def significant_count(a: list) -> int:
    """Challenge 1: pairs i < j with a[i] > 2 a[j], counted with a second pointer before each merge."""
    def go(v):
        if len(v) <= 1:
            return list(v), 0
        mid = len(v) // 2
        left, x = go(v[:mid])
        right, y = go(v[mid:])
        count, i = 0, 0
        for r in right:
            while i < len(left) and left[i] <= 2 * r:
                i += 1
            count += len(left) - i
        return sorted(left + right), x + y + count
    return go(a)[1]


def jumps(left: list, right: list) -> list:
    """The final merge of Figure 20.2: (value taken from the right, how many left values it jumps)."""
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            i += 1
        else:
            out.append((right[j], len(left) - i))
            j += 1
    return out


if __name__ == "__main__":
    print(inversions_brute(RANKS), sort_count(RANKS))
    print(closest_brute(BOXES), closest_pair(BOXES))
