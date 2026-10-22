"""Volume 7, Chapter 14 - Thinking Problem 2: the narrowest straight strip that holds every point.

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations

import math

from ch14_examples import BOXES, convex_hull, cross


def min_width(points: list) -> float:
    """Width of the narrowest strip between two parallel lines containing every point: O(n log n) for the hull,
    then O(h) rotating calipers, since a narrowest strip always has one side flush with a hull edge."""
    hull = convex_hull(points)
    h = len(hull)
    if h < 3:
        return 0.0                                  # no points, one point, or all in a line
    best, j = math.inf, 1
    for i in range(h):
        a, b = hull[i], hull[(i + 1) % h]
        while abs(cross(a, b, hull[(j + 1) % h])) > abs(cross(a, b, hull[j])):
            j = (j + 1) % h                         # the corner farthest from edge a-b
        best = min(best, abs(cross(a, b, hull[j])) / math.dist(a, b))
    return best


if __name__ == "__main__":
    print(round(min_width(BOXES), 3))
