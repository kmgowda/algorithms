"""Volume 7, Chapter 12 - Thinking Problem 2: are any three of n whole-number points in a line?

Run:  python3 ch12_solutions.py
"""

from __future__ import annotations

from math import gcd


def direction(p, q):
    """The direction from p to q, reduced and sign-normalised, so parallel vectors get the same key."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    g = gcd(dx, dy)
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):
        dx, dy = -dx, -dy
    return dx, dy


def three_in_a_line(points) -> bool:
    """True if some three of the points (repeats allowed) lie on one line. O(n^2) expected time."""
    pts = list(points)
    if len(pts) < 3:
        return False
    if len(set(pts)) < len(pts):
        return True                       # a repeated point is in line with any third point
    for i, p in enumerate(pts):
        seen = set()
        for q in pts[i + 1:]:
            d = direction(p, q)
            if d in seen:
                return True               # p, q and an earlier point share a line through p
            seen.add(d)
    return False


if __name__ == "__main__":
    town = [(0, 0), (4, 1), (2, 5), (3, 5), (10, 4)]
    print(three_in_a_line(town), three_in_a_line(town + [(8, 2)]))
