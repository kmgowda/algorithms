"""Volume 7, Chapter 15 - Areas and Insides of Polygons: the shoelace formula and the crossing count.

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

# The library's garden, corners in metres, walking anticlockwise.
GARDEN = [(0, 0), (8, 0), (8, 6), (4, 3), (0, 6)]


def area(poly: list) -> float:
    """Shoelace formula (Figure 15.2): half the sum of cross products of neighbouring corners. Positive if anticlockwise."""
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n)) / 2


def on_edge(p, a, b) -> bool:
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    return cross == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def inside(p, poly: list) -> str:
    """'inside', 'outside', or 'edge': count how many edges a ray to the right crosses (Figure 15.3)."""
    n, crossings = len(poly), 0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_edge(p, a, b):
            return "edge"
        if (a[1] > p[1]) != (b[1] > p[1]):           # the edge straddles the ray's height
            x = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                crossings += 1
    return "inside" if crossings % 2 else "outside"


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def inside_exact(p, poly: list) -> str:
    """The same ray test without division: an edge that straddles p's height (half-open: one end strictly above,
    the other at or below) crosses the ray to the right of p exactly when p is on the correct side of it."""
    n, crossings = len(poly), 0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_edge(p, a, b):
            return "edge"
        if (a[1] > p[1]) != (b[1] > p[1]):
            lower, upper = (a, b) if a[1] < b[1] else (b, a)
            if _cross(lower, upper, p) > 0:            # p is left of the upward edge, so the edge is to p's right
                crossings += 1
    return "inside" if crossings % 2 else "outside"


def winding_number(p, poly: list) -> int:
    """How many times the boundary winds anticlockwise round p (Figure 15.4): +1 for each upward edge passing to the
    right of p, -1 for each downward one. 0 means outside; for simple polygons it is +1 or -1 inside."""
    w, n = 0, len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if a[1] <= p[1] < b[1] and _cross(a, b, p) > 0:
            w += 1
        elif b[1] <= p[1] < a[1] and _cross(a, b, p) < 0:
            w -= 1
    return w


def inside_convex(p, poly: list) -> tuple[str, int]:
    """Point in a convex polygon (anticlockwise, n >= 3) in O(log n): binary search the fan of triangles from corner 0
    for the wedge holding p, then one turn test. Returns (verdict, turn tests)."""
    n, tests = len(poly), 0
    o = poly[0]
    tests += 2
    if _cross(o, poly[1], p) < 0 or _cross(o, poly[-1], p) > 0:
        return "outside", tests
    lo, hi = 1, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        tests += 1
        if _cross(o, poly[mid], p) >= 0:
            lo = mid
        else:
            hi = mid
    tests += 1
    c = _cross(poly[lo], poly[lo + 1], p)
    if c < 0:
        return "outside", tests
    if c == 0 or (lo == 1 and _cross(o, poly[1], p) == 0) or (lo == n - 2 and _cross(o, poly[-1], p) == 0):
        return "edge", tests                                   # on the far edge, or on one of the two edges at corner 0
    return "inside", tests


def boundary_points(poly: list) -> int:
    """Whole-number points on the boundary: gcd(|dx|, |dy|) per edge (each corner counted once)."""
    import math
    n = len(poly)
    return sum(math.gcd(abs(poly[(i + 1) % n][0] - poly[i][0]), abs(poly[(i + 1) % n][1] - poly[i][1])) for i in range(n))


def interior_points_by_pick(poly: list) -> int:
    """Pick's theorem: area = interior + boundary / 2 - 1."""
    return int(abs(area(poly)) - boundary_points(poly) / 2 + 1)


def interior_points_by_testing(poly: list) -> int:
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return sum(1 for x in range(min(xs), max(xs) + 1) for y in range(min(ys), max(ys) + 1) if inside_exact((x, y), poly) == "inside")


STAR = [(0, 6), (12, -4), (7, 12), (2, -4), (14, 6)]      # a five-pointed star drawn in one stroke, anticlockwise


if __name__ == "__main__":
    print(area(GARDEN), area(GARDEN[::-1]))
    for p in ((2, 2), (4, 5), (8, 3), (4, 3), (6, 1), (9, 1), (2, 6), (6, 4)):
        print(p, inside(p, GARDEN), inside_exact(p, GARDEN), winding_number(p, GARDEN))
    print(boundary_points(GARDEN), interior_points_by_pick(GARDEN), interior_points_by_testing(GARDEN))
    centre = (7, 4)
    print(area(STAR), winding_number(centre, STAR), inside_exact(centre, STAR), winding_number((7, 9), STAR), inside_exact((7, 9), STAR))
    hexagon = [(4, 0), (8, 2), (8, 6), (4, 8), (0, 6), (0, 2)]
    print([inside_convex(p, hexagon) for p in ((4, 4), (9, 4), (8, 4), (1, 1))])
