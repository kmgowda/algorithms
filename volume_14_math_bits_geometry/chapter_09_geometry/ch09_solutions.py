"""Volume 14, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch09_examples import Point, convex_hull, cross


def is_convex(polygon: list[Point]) -> bool:
    """Exercise 1 (LeetCode 469): convex if every turn has the same direction (ignoring straight ones)."""
    signs = set()
    n = len(polygon)
    for i in range(n):
        c = cross(polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n])
        if c:
            signs.add(c > 0)
    return len(signs) <= 1


def max_points_on_line(points: list[Point]) -> int:
    """Exercise 2 (LeetCode 149): for each point, group the others by reduced direction (dy, dx)."""
    if len(points) <= 2:
        return len(points)
    best = 0
    for i, (x1, y1) in enumerate(points):
        slopes: dict[tuple[int, int], int] = {}
        for x2, y2 in points[i + 1:]:
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            slopes[(dx, dy)] = slopes.get((dx, dy), 0) + 1
        best = max(best, 1 + max(slopes.values(), default=0))
    return best


def fence_trees(trees: list[Point]) -> list[Point]:
    """Exercise 3 (LeetCode 587): every tree ON the fence, including those in the middle of a straight side -
    keep collinear points by popping only on strict right turns."""
    pts = sorted(set(trees))
    if len(pts) <= 2:
        return pts

    def half(seq: list[Point]) -> list[Point]:
        chain: list[Point] = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) < 0:
                chain.pop()
            chain.append(p)
        return chain

    return sorted(set(half(pts) + half(pts[::-1])))


def hull_size(points: list[Point]) -> int:
    """Exercise 4: how many corners the convex hull has."""
    return len(convex_hull(points))


if __name__ == "__main__":
    print(is_convex([(0, 0), (4, 0), (4, 4), (0, 4)]), is_convex([(0, 0), (4, 0), (1, 1), (0, 4)]),
          max_points_on_line([(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)]),
          fence_trees([(1, 1), (2, 2), (2, 0), (2, 4), (3, 3), (4, 2)]))
