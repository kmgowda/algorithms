"""Volume 6, Chapter 13 - Do Two Segments Cross? Four turn tests, plus care for touching and overlapping.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import itertools


def cross(o, a, b) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p, q, r) -> bool:
    """r lies within the bounding box of p, q (used once r is known to be in line with them)."""
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def segments_cross(p1, p2, q1, q2) -> bool:
    """True if segment p1-p2 and segment q1-q2 share at least one point (Figure 13.2)."""
    d1, d2 = cross(q1, q2, p1), cross(q1, q2, p2)
    d3, d4 = cross(p1, p2, q1), cross(p1, p2, q2)
    if ((d1 > 0) != (d2 > 0)) and d1 and d2 and ((d3 > 0) != (d4 > 0)) and d3 and d4:
        return True                                   # each segment's ends lie on opposite sides of the other
    return ((d1 == 0 and on_segment(q1, q2, p1)) or (d2 == 0 and on_segment(q1, q2, p2)) or
            (d3 == 0 and on_segment(p1, p2, q1)) or (d4 == 0 and on_segment(p1, p2, q2)))


# Planned cycle paths in the park, as segments.
PATHS = {"A": ((0, 0), (6, 4)), "B": ((0, 4), (6, 0)), "C": ((1, 5), (5, 5)), "D": ((6, 4), (8, 1)), "E": ((2, 0), (4, 0))}


def crossing_pairs(paths: dict) -> list:
    return [(a, b) for a, b in itertools.combinations(sorted(paths), 2) if segments_cross(*paths[a], *paths[b])]


if __name__ == "__main__":
    print(crossing_pairs(PATHS))
    print(segments_cross((0, 0), (4, 0), (2, 0), (6, 0)), segments_cross((0, 0), (2, 0), (3, 0), (5, 0)), segments_cross((0, 0), (2, 2), (2, 2), (4, 0)),
          segments_cross((0, 0), (2, 2), (3, 3), (5, 5)), segments_cross((1, 1), (1, 1), (0, 0), (2, 2)))
