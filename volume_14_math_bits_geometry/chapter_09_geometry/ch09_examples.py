"""Volume 14, Chapter 9 - Computational Geometry: Points, Lines, Convex Hull.

Integer coordinates keep every test exact (no floating-point surprises, Chapter 1).

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import math

Point = tuple[int, int]


def cross(o: Point, a: Point, b: Point) -> int:
    """Cross product of OA and OB: > 0 if O -> A -> B turns left (counter-clockwise), < 0 right, 0 straight."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def orientation(o: Point, a: Point, b: Point) -> str:
    c = cross(o, a, b)
    return "left" if c > 0 else "right" if c < 0 else "straight"


def on_segment(p: Point, a: Point, b: Point) -> bool:
    """Is p on the segment ab? Collinear and inside the bounding box."""
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Do segments ab and cd touch? Each segment's ends must lie on opposite sides of the other (or touch it)."""
    d1, d2 = cross(c, d, a), cross(c, d, b)
    d3, d4 = cross(a, b, c), cross(a, b, d)
    if (d1 > 0) != (d2 > 0) and (d3 > 0) != (d4 > 0) and d1 and d2 and d3 and d4:
        return True
    return on_segment(a, c, d) or on_segment(b, c, d) or on_segment(c, a, b) or on_segment(d, a, b)


def polygon_area(points: list[Point]) -> float:
    """Shoelace formula: half the absolute sum of cross products of consecutive vertices."""
    s = sum(points[i][0] * points[i - 1][1] - points[i - 1][0] * points[i][1] for i in range(len(points)))
    return abs(s) / 2


def convex_hull(points: list[Point]) -> list[Point]:
    """Andrew's monotone chain: sort, then build the lower and upper hulls, popping points that make a right turn.
    O(n log n). Returns the hull counter-clockwise without repeating the first point."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def half(seq: list[Point]) -> list[Point]:
        chain: list[Point] = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        return chain

    lower, upper = half(pts), half(pts[::-1])
    return lower[:-1] + upper[:-1]


def point_in_polygon(p: Point, polygon: list[Point]) -> str:
    """Ray casting: count how many edges a ray going right from p crosses - odd means inside."""
    inside = False
    for i in range(len(polygon)):
        a, b = polygon[i - 1], polygon[i]
        if on_segment(p, a, b):
            return "boundary"
        if (a[1] > p[1]) != (b[1] > p[1]):
            x_cross = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if p[0] < x_cross:
                inside = not inside
    return "inside" if inside else "outside"


def delivery_zone(stops: list[Point]) -> tuple[list[Point], float, float]:
    """Industry example: the smallest convex region containing all delivery stops, its area and fence length."""
    hull = convex_hull(stops)
    perimeter = sum(math.dist(hull[i - 1], hull[i]) for i in range(len(hull)))
    return hull, polygon_area(hull), perimeter


if __name__ == "__main__":
    print(orientation((0, 0), (4, 0), (4, 3)), orientation((0, 0), (4, 0), (8, 0)))
    print(segments_intersect((0, 0), (4, 4), (0, 4), (4, 0)), segments_intersect((0, 0), (1, 1), (2, 2), (3, 3)))
    print(polygon_area([(0, 0), (4, 0), (4, 3), (0, 3)]))
    pts = [(0, 0), (2, 1), (4, 0), (3, 2), (4, 4), (1, 3), (0, 4), (2, 2)]
    print(convex_hull(pts))
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    print([point_in_polygon(p, square) for p in [(2, 2), (5, 1), (4, 2)]])
    print(delivery_zone([(1, 1), (6, 2), (5, 7), (2, 6), (3, 3), (4, 4)]))
