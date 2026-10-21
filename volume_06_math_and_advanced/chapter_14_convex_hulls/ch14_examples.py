"""Volume 6, Chapter 14 - Convex Hulls: the shortest fence around every point (Andrew's monotone chain).

Run:  python3 ch14_examples.py
"""

from __future__ import annotations

import itertools
import math
import random

# Book-drop boxes around town (Volume 4, Chapter 20).
BOXES = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), (20, 25), (35, 8)]


def cross(o, a, b) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list) -> list:
    """Corners of the hull, anticlockwise from the lowest-left point (Figure 14.2). Points in a line on an edge are left out."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()                               # not a left turn: the middle point is inside
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def perimeter(hull: list) -> float:
    return sum(math.dist(hull[i], hull[(i + 1) % len(hull)]) for i in range(len(hull))) if len(hull) > 1 else 0.0


def encloses(hull: list, points: list) -> bool:
    """Every point is inside or on the hull, and the hull turns left at every corner."""
    n = len(hull)
    if n < 3:
        return True
    left = all(cross(hull[i], hull[(i + 1) % n], hull[(i + 2) % n]) > 0 for i in range(n))
    return left and all(cross(hull[i], hull[(i + 1) % n], p) >= 0 for p in points for i in range(n))


if __name__ == "__main__":
    h = convex_hull(BOXES)
    print(h, round(perimeter(h), 2))
    print(convex_hull([]), convex_hull([(1, 1)]), convex_hull([(1, 1), (1, 1)]), convex_hull([(0, 0), (1, 1), (2, 2)]), convex_hull([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (2, 0)]))
    r = random.Random(14)
    pts = [(r.randint(0, 1000), r.randint(0, 1000)) for _ in range(10000)]
    print(len(convex_hull(pts)))
