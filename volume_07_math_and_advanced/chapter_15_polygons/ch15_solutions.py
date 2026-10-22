"""Volume 7, Chapter 15 - Thinking Problem 2: is a polygon strictly convex? O(n), exact, and not fooled by stars.

Run:  python3 ch15_solutions.py
"""

from __future__ import annotations

from ch15_examples import GARDEN, STAR, _cross


def _upper(d) -> bool:
    """Direction angle in [0, 180 degrees): above the x-axis, or pointing straight right."""
    return d[1] > 0 or (d[1] == 0 and d[0] > 0)


def is_convex(poly: list) -> bool:
    """True if the corners (either orientation) form a strictly convex polygon: every turn is the same strict turn,
    and the edge direction goes round exactly once (a one-stroke star turns the same way but goes round twice)."""
    n = len(poly)
    if n < 3:
        return False
    turns = [_cross(poly[i - 1], poly[i], poly[(i + 1) % n]) for i in range(n)]
    if all(t < 0 for t in turns):
        poly = [(-x, y) for x, y in poly]           # a mirror image turns a clockwise list anticlockwise
    elif not all(t > 0 for t in turns):
        return False
    dirs = [(poly[(i + 1) % n][0] - poly[i][0], poly[(i + 1) % n][1] - poly[i][1]) for i in range(n)]
    wraps = sum(1 for i in range(n) if not _upper(dirs[i]) and _upper(dirs[(i + 1) % n]))
    return wraps == 1


if __name__ == "__main__":
    hexagon = [(4, 0), (8, 2), (8, 6), (4, 8), (0, 6), (0, 2)]
    print(is_convex(GARDEN), is_convex(STAR), is_convex(hexagon), is_convex(hexagon[::-1]))
