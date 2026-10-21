"""Volume 6, Chapter 16 - Sweep Lines: move a line across the plane and only handle events.

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
    """Area covered by rectangles: sweep left to right; between events, covered height x width (Figure 16.2)."""
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
    """Closest pair by sweeping x, comparing only points within the best distance so far. Returns (distance², comparisons)."""
    pts = sorted(points)
    best, comps, start = float("inf"), 0, 0
    for i, p in enumerate(pts):
        while (p[0] - pts[start][0]) ** 2 > best:
            start += 1
        for q in pts[start:i]:
            comps += 1
            best = min(best, (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
    return best, comps


if __name__ == "__main__":
    print(max_overlap(BOOKINGS), union_area(TABLES), union_area_by_cells(TABLES))
    import random
    r = random.Random(16)
    pts = [(r.randint(0, 10 ** 6), r.randint(0, 10 ** 6)) for _ in range(3000)]
    d, comps = closest_by_sweep(pts)
    print(d, comps, 3000 * 2999 // 2)
