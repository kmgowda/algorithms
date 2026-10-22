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


def intersection_point(p1, p2, q1, q2):
    """Where two segments that cross at a single point meet, as exact fractions (Figure 13.4); None if they are
    parallel (including overlapping pieces of one line) or do not meet."""
    from fractions import Fraction
    r = (p2[0] - p1[0], p2[1] - p1[1])
    s_ = (q2[0] - q1[0], q2[1] - q1[1])
    denom = r[0] * s_[1] - r[1] * s_[0]
    if denom == 0 or not segments_cross(p1, p2, q1, q2):
        return None
    w = (q1[0] - p1[0], q1[1] - p1[1])
    t = Fraction(w[0] * s_[1] - w[1] * s_[0], denom)
    return (p1[0] + t * r[0], p1[1] + t * r[1])


def _y_at(seg, x):
    """Height of a non-vertical segment at the sweep position x, as an exact fraction."""
    from fractions import Fraction
    (x1, y1), (x2, y2) = seg
    return Fraction(y1) + Fraction(y2 - y1, x2 - x1) * (x - x1)


def any_crossing(segments: list) -> tuple[tuple | None, int]:
    """Shamos-Hoey sweep (Figure 13.5): is there any pair of crossing segments? Sweep left to right; keep the
    segments the line currently cuts in order of height (the status); only neighbours in that order are tested.
    Segments must not be vertical. Returns (a crossing pair of indices or None, pair tests made).
    The status is a sorted Python list (simple); a balanced search tree makes each step O(log n)."""
    import bisect
    segs = [tuple(sorted(sg)) for sg in segments]
    if any(a[0] == b[0] for a, b in segs):
        raise ValueError("this sweep assumes no vertical segments")
    events = []
    for i, (a, b) in enumerate(segs):
        events.append((a[0], 0, a[1], i))          # left end: kind 0 comes first at equal x
        events.append((b[0], 1, b[1], i))          # right end
    events.sort()
    status, tests = [], 0

    def test(i, j):
        nonlocal tests
        tests += 1
        return segments_cross(*segs[i], *segs[j])

    for x, kind, _, i in events:
        if kind == 0:
            keys = [(_y_at(segs[j], x), j) for j in status]
            key = (_y_at(segs[i], x), i)
            pos = bisect.bisect_left(keys, key)
            status.insert(pos, i)
            for nb in (pos - 1, pos + 1):
                if 0 <= nb < len(status) and test(i, status[nb]):
                    return (min(i, status[nb]), max(i, status[nb])), tests
        else:
            pos = status.index(i)
            if 0 < pos < len(status) - 1 and test(status[pos - 1], status[pos + 1]):
                a, b = status[pos - 1], status[pos + 1]
                return (min(a, b), max(a, b)), tests
            status.pop(pos)
    return None, tests


def any_crossing_brute(segments: list) -> bool:
    return any(segments_cross(*a, *b) for a, b in itertools.combinations(segments, 2))


# Planned cycle paths in the park, as segments.
PATHS = {"A": ((0, 0), (6, 4)), "B": ((0, 4), (6, 0)), "C": ((1, 5), (5, 5)), "D": ((6, 4), (8, 1)), "E": ((2, 0), (4, 0))}


def crossing_pairs(paths: dict) -> list:
    return [(a, b) for a, b in itertools.combinations(sorted(paths), 2) if segments_cross(*paths[a], *paths[b])]


if __name__ == "__main__":
    print(crossing_pairs(PATHS))
    print(segments_cross((0, 0), (4, 0), (2, 0), (6, 0)), segments_cross((0, 0), (2, 0), (3, 0), (5, 0)), segments_cross((0, 0), (2, 2), (2, 2), (4, 0)),
          segments_cross((0, 0), (2, 2), (3, 3), (5, 5)), segments_cross((1, 1), (1, 1), (0, 0), (2, 2)))
    print(intersection_point(*PATHS["A"], *PATHS["B"]), intersection_point(*PATHS["A"], *PATHS["D"]), intersection_point((1, 1), (7, 3), *PATHS["B"]))
    nonvert = [PATHS[k] for k in ("A", "B", "C", "D", "E")]
    print(any_crossing(nonvert), any_crossing([PATHS["C"], PATHS["E"]]))
    import random
    r = random.Random(13)
    sg = []
    while len(sg) < 2000:
        a = (r.randint(0, 10 ** 6), r.randint(0, 10 ** 6))
        b = (a[0] + r.randint(1, 3000), a[1] + r.randint(-3000, 3000))
        sg.append((a, b))
    print(any_crossing(sg), len(sg) * (len(sg) - 1) // 2)
    shelves = [((r.randint(0, 500), 3 * k), (r.randint(600, 1200), 3 * k + 1)) for k in range(2000)]
    print(any_crossing(shelves), any_crossing_brute(shelves[:300]))
