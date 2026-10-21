"""Volume 6, Chapter 12 - Points, Vectors, and Turns: the cross product tells left from right.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import math

# Drop boxes on the town grid (hundreds of metres east, north), from Volume 4, Chapter 20.
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


if __name__ == "__main__":
    u, v = sub(PARK, LIBRARY), sub(MARKET, LIBRARY)
    print(u, v, dot(u, v), cross(u, v), round(angle_degrees(u, v), 1))
    print(turn(LIBRARY, PARK, MARKET), turn(LIBRARY, MARKET, PARK), turn((0, 0), (1, 1), (3, 3)))
    print(round(distance(LIBRARY, MARKET), 3), triangle_area(LIBRARY, PARK, MARKET))
