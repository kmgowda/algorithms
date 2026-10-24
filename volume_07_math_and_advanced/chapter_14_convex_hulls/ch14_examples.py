"""Volume 7, Chapter 14 - Convex Hulls: the shortest fence around every point (Andrew's monotone chain).

Run:  python3 ch14_examples.py
"""

from __future__ import annotations

import itertools
import math
import random

# Book-drop boxes around town (Volume 5, Chapter 22).
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


def graham_scan(points: list, log: list | None = None) -> list:
    """Graham's scan (Figure 14.3): start from the lowest point, sort the others by angle around it (by cross-product
    comparisons, no trigonometry; nearer first when in line), and keep a stack that always turns left."""
    import functools
    pts = sorted(set(points), key=lambda p: (p[1], p[0]))
    if len(pts) <= 2:
        return pts
    o = pts[0]

    def by_angle(a, b):
        c = cross(o, a, b)
        if c:
            return -1 if c > 0 else 1
        da = (a[0] - o[0]) ** 2 + (a[1] - o[1]) ** 2
        db = (b[0] - o[0]) ** 2 + (b[1] - o[1]) ** 2
        return -1 if da < db else (1 if da > db else 0)

    rest = sorted(pts[1:], key=functools.cmp_to_key(by_angle))
    stack = [o]
    for p in rest:
        while len(stack) >= 2 and cross(stack[-2], stack[-1], p) <= 0:
            popped = stack.pop()
            if log is not None:
                log.append(("pop", popped, p))
        stack.append(p)
        if log is not None:
            log.append(("push", p))
    return stack


def jarvis_march(points: list) -> tuple[list, int]:
    """Gift wrapping (Figure 14.3): from the leftmost point, repeatedly take the point with every other point to its left.
    Returns (hull anticlockwise, cross-product tests); the cost is about n times the number of corners."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts, 0
    hull, tests = [], 0
    start = pts[0]
    p = start
    while True:
        hull.append(p)
        q = pts[0] if pts[0] != p else pts[1]
        for r in pts:
            if r == p:
                continue
            tests += 1
            c = cross(p, q, r)
            far = (r[0] - p[0]) ** 2 + (r[1] - p[1]) ** 2 > (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
            if c < 0 or (c == 0 and far):
                q = r                                  # r is to the right of p->q (or further along it): wrap tighter
        p = q
        if p == start:
            return hull, tests


def rotate_hull(hull: list) -> list:
    """The same corners starting from the lowest-left point, anticlockwise (to compare hulls from different methods)."""
    if not hull:
        return hull
    k = hull.index(min(hull))
    return hull[k:] + hull[:k]


def diameter_brute(hull: list) -> tuple[float, tuple, tuple]:
    best = (0.0, None, None)
    for i in range(len(hull)):
        for j in range(i + 1, len(hull)):
            d = math.dist(hull[i], hull[j])
            if d > best[0]:
                best = (d, hull[i], hull[j])
    return best


def rotating_calipers(hull: list) -> tuple[float, tuple, tuple, int]:
    """Farthest pair of a convex polygon (anticlockwise corners) in O(h): for each edge, advance the opposite pointer
    while the triangle area grows; the farthest pair is among the "antipodal" pairs met. Returns (d, p, q, steps)."""
    h = len(hull)
    if h == 1:
        return 0.0, hull[0], hull[0], 0
    if h == 2:
        return math.dist(hull[0], hull[1]), hull[0], hull[1], 0
    best, steps, j = (0.0, None, None), 0, 1
    for i in range(h):
        a, b = hull[i], hull[(i + 1) % h]
        while abs(cross(a, b, hull[(j + 1) % h])) > abs(cross(a, b, hull[j])):
            j = (j + 1) % h
            steps += 1
        for p in (a, b):
            d = math.dist(p, hull[j])
            steps += 1
            if d > best[0]:
                best = (d, p, hull[j])
    return best[0], best[1], best[2], steps


def perimeter(hull: list) -> float:
    return sum(math.dist(hull[i], hull[(i + 1) % len(hull)]) for i in range(len(hull))) if len(hull) > 1 else 0.0


def encloses(hull: list, points: list) -> bool:
    """Every point is inside or on the hull, and the hull turns left at every corner."""
    n = len(hull)
    if n < 3:
        return True
    left = all(cross(hull[i], hull[(i + 1) % n], hull[(i + 2) % n]) > 0 for i in range(n))
    return left and all(cross(hull[i], hull[(i + 1) % n], p) >= 0 for p in points for i in range(n))


BRANCHES = [(1, 1), (6, 1), (4, 4), (1, 6), (7, 6), (3, 8)]   # library branches on the town grid (Section 14.7)


def in_circle(a, b, c, d) -> int:
    """Positive when d lies strictly inside the circle through a, b, c (taken anticlockwise): a 3 x 3 determinant
    of the points lifted onto the bowl z = x^2 + y^2."""
    rows = [(p[0] - d[0], p[1] - d[1], (p[0] - d[0]) ** 2 + (p[1] - d[1]) ** 2) for p in (a, b, c)]
    (a1, a2, a3), (b1, b2, b3), (c1, c2, c3) = rows
    return a1 * (b2 * c3 - b3 * c2) - a2 * (b1 * c3 - b3 * c1) + a3 * (b1 * c2 - b2 * c1)


def delaunay_brute(points: list) -> list:
    """Every triangle whose circumcircle has no other point strictly inside: the Delaunay triangulation (for points
    with no four on a circle). O(n^4), for checking; Fortune's sweep or flips build it in O(n log n)."""
    import itertools
    tris = []
    for a, b, c in itertools.combinations(points, 3):
        o = cross(a, b, c)
        if o == 0:
            continue
        if o < 0:
            b, c = c, b
        if all(in_circle(a, b, c, d) <= 0 for d in points if d not in (a, b, c)):
            tris.append(tuple(sorted((a, b, c))))
    return sorted(tris)


def nearest_branch(points: list, q) -> tuple:
    """The Voronoi question: which branch is nearest to q? (Brute force; the Voronoi diagram answers it by
    looking up the region q falls in.)"""
    return min(points, key=lambda p: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


if __name__ == "__main__":
    h = convex_hull(BOXES)
    print(h, round(perimeter(h), 2))
    print(convex_hull([]), convex_hull([(1, 1)]), convex_hull([(1, 1), (1, 1)]), convex_hull([(0, 0), (1, 1), (2, 2)]), convex_hull([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (2, 0)]))
    r = random.Random(14)
    pts = [(r.randint(0, 1000), r.randint(0, 1000)) for _ in range(10000)]
    print(len(convex_hull(pts)))
    log = []
    g = graham_scan(BOXES, log)
    print(g, log)
    jh, tests = jarvis_march(BOXES)
    print(jh, tests, rotate_hull(jh) == rotate_hull(h), rotate_hull(g) == rotate_hull(h))
    print(diameter_brute(h), rotating_calipers(h))
    r2 = random.Random(140)
    cont = [(r2.random(), r2.random()) for _ in range(10000)]
    print(len(convex_hull(cont)), round(8 / 3 * math.log(10000), 1), jarvis_march(pts)[1], len(convex_hull(pts)) * 10000)
    print(delaunay_brute(BRANCHES), len(convex_hull(BRANCHES)))
