"""Volume 6, Chapter 15 - Areas and Insides of Polygons: the shoelace formula and the crossing count.

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


if __name__ == "__main__":
    print(area(GARDEN), area(GARDEN[::-1]))
    for p in ((2, 2), (4, 5), (8, 3), (4, 3), (6, 1), (9, 1), (2, 6)):
        print(p, inside(p, GARDEN))
