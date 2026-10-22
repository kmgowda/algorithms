"""Volume 7, Chapter 16 - Sweep Lines: move a line across the plane and only handle events.

Run:  python3 ch16_examples.py
"""

from __future__ import annotations

import itertools

# Room bookings as intervals on a time line (hours), and reading-table rectangles (x1, y1, x2, y2) in metres.
BOOKINGS = [(9, 11), (10, 12), (11, 13), (9, 15), (12, 14), (13, 16), (14, 15), (15, 17)]
TABLES = [(0, 0, 4, 2), (2, 1, 6, 3), (5, 0, 7, 2)]


def max_overlap(intervals: list) -> tuple[int, int]:
    """Sweep the time line: +1 at each start, -1 at each end (ends before starts at the same time).
    Returns (largest overlap, events handled)."""
    events = sorted([(s, 1) for s, _ in intervals] + [(e, -1) for _, e in intervals], key=lambda ev: (ev[0], ev[1]))
    now = best = 0
    for _, d in events:
        now += d
        best = max(best, now)
    return best, len(events)


def union_area(rects: list) -> int:
    """Area covered by rectangles: sweep left to right; between events, covered height x width (Figure 16.1)."""
    xs = sorted({x for r in rects for x in (r[0], r[2])})
    total = 0
    for a, b in zip(xs, xs[1:]):
        spans = sorted((r[1], r[3]) for r in rects if r[0] <= a and r[2] >= b)
        covered, top = 0, None
        for lo, hi in spans:
            if top is None or lo > top:
                covered += hi - lo
                top = hi
            elif hi > top:
                covered += hi - top
                top = hi
        total += covered * (b - a)
    return total


def union_area_by_cells(rects: list) -> int:
    return len({(x, y) for x1, y1, x2, y2 in rects for x in range(x1, x2) for y in range(y1, y2)})


def closest_by_sweep(points: list) -> tuple[float, int]:
    """The x-strip shortcut: compare only points within the best distance so far behind the line. Fast on spread-out
    points, but O(n^2) when many points share nearly the same x (Figure 16.3). Returns (distance squared, comparisons)."""
    pts = sorted(points)
    best, comps, start = float("inf"), 0, 0
    for i, p in enumerate(pts):
        while (p[0] - pts[start][0]) ** 2 > best:
            start += 1
        for q in pts[start:i]:
            comps += 1
            best = min(best, (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
    return best, comps


def closest_pair_sweep(points: list) -> tuple[float, int]:
    """Closest pair by a sweep with a y-ordered status (Figure 16.3): keep the points within d (the best distance so
    far) behind the line, ordered by y, and compare the new point only with those within d above or below it.
    O(n log n) with a balanced tree; the companion uses a sorted list. Returns (distance squared, comparisons)."""
    import bisect
    import math
    pts = sorted(points)
    if len(pts) < 2:
        return float("inf"), 0
    best, comps, left = float("inf"), 0, 0
    active = []                                        # (y, x) of the points in the strip, sorted by y
    for p in pts:
        d = math.sqrt(best)
        while left < len(pts) and pts[left][0] < p[0] - d:
            q = pts[left]
            active.pop(bisect.bisect_left(active, (q[1], q[0])))
            left += 1
        lo = bisect.bisect_left(active, (p[1] - d, -math.inf))
        hi = bisect.bisect_right(active, (p[1] + d, math.inf))
        for y, x in active[lo:hi]:
            comps += 1
            best = min(best, (p[0] - x) ** 2 + (p[1] - y) ** 2)
        bisect.insort(active, (p[1], p[0]))
    return best, comps


def closest_brute(points: list) -> float:
    return min(((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in itertools.combinations(points, 2)), default=float("inf"))


def strip_heights(rects: list) -> list:
    """For each strip between neighbouring events: (left x, right x, covered height) (Figure 16.1)."""
    xs = sorted({x for r in rects for x in (r[0], r[2])})
    out = []
    for a, b in zip(xs, xs[1:]):
        spans = sorted((r[1], r[3]) for r in rects if r[0] <= a and r[2] >= b)
        covered, top = 0, None
        for lo, hi in spans:
            if top is None or lo > top:
                covered, top = covered + hi - lo, hi
            elif hi > top:
                covered, top = covered + hi - top, hi
        out.append((a, b, covered))
    return out


def skyline(buildings: list) -> list:
    """The outline of buildings (left, right, height) on a street: sweep left to right with a max-heap of the heights
    standing over the line; record a key point (x, height) whenever the tallest height changes."""
    import heapq
    events = sorted({x for l, r, _ in buildings for x in (l, r)})
    by_left = sorted(buildings)
    heap, out, i = [], [], 0                         # heap of (-height, right end)
    for x in events:
        while i < len(by_left) and by_left[i][0] <= x:
            l, r, h = by_left[i]
            heapq.heappush(heap, (-h, r))
            i += 1
        while heap and heap[0][1] <= x:
            heapq.heappop(heap)
        h = -heap[0][0] if heap else 0
        if not out or out[-1][1] != h:
            out.append((x, h))
    return out


if __name__ == "__main__":
    print(max_overlap(BOOKINGS), union_area(TABLES), union_area_by_cells(TABLES))
    import random
    r = random.Random(16)
    pts = [(r.randint(0, 10 ** 6), r.randint(0, 10 ** 6)) for _ in range(3000)]
    d, comps = closest_by_sweep(pts)
    print(d, comps, 3000 * 2999 // 2)
    print(closest_pair_sweep(pts))
    line_pts = [(0, 3 * i) for i in range(2000)]
    print(closest_by_sweep(line_pts), closest_pair_sweep(line_pts))
    print(strip_heights(TABLES), skyline([(1, 5, 3), (2, 4, 6), (3, 9, 2), (7, 8, 4)]))
