"""Volume 7, Chapter 12 - Points, Vectors, and Turns: the cross product tells left from right.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import math

# Drop boxes on the town grid (hundreds of metres east, north), from Volume 5, Chapter 22.
LIBRARY, PARK, MARKET = (0, 0), (4, 1), (2, 5)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(u, v) -> int:
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v) -> int:
    """Positive if v is to the left of u, negative if to the right, zero if in line (Figure 12.2)."""
    return u[0] * v[1] - u[1] * v[0]


def turn(a, b, c) -> str:
    """Walking a -> b -> c: which way do you turn at b?"""
    k = cross(sub(b, a), sub(c, b))
    return "left" if k > 0 else "right" if k < 0 else "straight"


def angle_degrees(u, v) -> float:
    if u == (0, 0) or v == (0, 0):
        raise ValueError("a zero vector has no direction")
    return math.degrees(math.atan2(cross(u, v), dot(u, v)))


def distance(a, b) -> float:
    return math.dist(a, b)


def triangle_area(a, b, c) -> float:
    return abs(cross(sub(b, a), sub(c, a))) / 2


def projection(p, a, b):
    """The point of the line through a and b closest to p, and the parameter t (0 at a, 1 at b) (Figure 12.3)."""
    u, w = sub(b, a), sub(p, a)
    if u == (0, 0):
        raise ValueError("a line needs two different points")
    t = dot(w, u) / dot(u, u)
    return (a[0] + t * u[0], a[1] + t * u[1]), t


def distance_to_line(p, a, b) -> float:
    """|cross(b - a, p - a)| / |b - a|: twice the triangle's area divided by its base."""
    u = sub(b, a)
    return abs(cross(u, sub(p, a))) / math.hypot(*u)


def distance_to_segment(p, a, b) -> float:
    """Like the line distance, but the foot is clamped to the segment's ends."""
    if a == b:
        return distance(p, a)
    foot, t = projection(p, a, b)
    if t <= 0:
        return distance(p, a)
    if t >= 1:
        return distance(p, b)
    return distance(p, foot)


def turn_sign(a, b, c) -> int:
    k = cross(sub(b, a), sub(c, b))
    return (k > 0) - (k < 0)


def exact_turn_sign(a, b, c) -> int:
    """The same test on the exact values of the inputs (floats converted to fractions without rounding)."""
    from fractions import Fraction
    fa, fb, fc = [(Fraction(x), Fraction(y)) for x, y in (a, b, c)]
    return turn_sign(fa, fb, fc)


def turn_with_tolerance(a, b, c, eps: float = 1e-9) -> str:
    """Treat a cross product smaller than eps times the lengths involved as "straight" (a relative tolerance)."""
    u, v = sub(b, a), sub(c, b)
    k = cross(u, v)
    scale = math.hypot(*u) * math.hypot(*v)
    if abs(k) <= eps * scale:
        return "straight"
    return "left" if k > 0 else "right"


if __name__ == "__main__":
    u, v = sub(PARK, LIBRARY), sub(MARKET, LIBRARY)
    print(u, v, dot(u, v), cross(u, v), round(angle_degrees(u, v), 1))
    print(turn(LIBRARY, PARK, MARKET), turn(LIBRARY, MARKET, PARK), turn((0, 0), (1, 1), (3, 3)))
    print(round(distance(LIBRARY, MARKET), 3), triangle_area(LIBRARY, PARK, MARKET))
    school, river_a, river_b = (3, 5), (0, 2), (10, 4)
    print(projection(school, river_a, river_b), round(distance_to_line(school, river_a, river_b), 3), round(distance_to_segment((12, 3), river_a, river_b), 3))
    tri = ((0.1, 0.3), (0.2, 0.6), (0.3, 0.9))
    print(cross(sub(tri[1], tri[0]), sub(tri[2], tri[1])), turn_sign(*tri), turn_with_tolerance(*tri))
    from fractions import Fraction as F
    print(turn_sign(*[(F(str(x)), F(str(y))) for x, y in tri]))
    a, b, c = (0.5 + 10 * 2 ** -53, 0.5), (12.0, 12.0), (24.0, 24.0)
    print(a, [turn_sign(a, b, c), turn_sign(b, c, a), turn_sign(c, a, b)], [exact_turn_sign(a, b, c), exact_turn_sign(b, c, a), exact_turn_sign(c, a, b)])
