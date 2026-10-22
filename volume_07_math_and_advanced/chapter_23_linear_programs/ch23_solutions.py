"""Volume 7, Chapter 23 - model solution to the design Thinking Problem: the largest round table in the room.

Run:  python3 ch23_solutions.py
"""

from __future__ import annotations

import math
from fractions import Fraction

from ch23_examples import best_corner


def largest_table(A: list, b: list):
    """Centre (x, y) and radius r of the largest circle inside {A (x, y) <= b, x >= 0, y >= 0}.
    A linear program in (x, y, r): a.(x, y) + r |a| <= b for every wall, and r <= x, r <= y for the two axes."""
    rows, bounds = [], []
    for (p, q), t in zip(A, b):
        rows.append([p, q, Fraction(math.hypot(p, q))])
        bounds.append(t)
    rows += [[-1, 0, 1], [0, -1, 1]]
    bounds += [0, 0]
    found = best_corner(rows, bounds, [0, 0, 1])
    if found is None:
        return None
    r, (x, y, _) = found
    return x, y, r


if __name__ == "__main__":
    print(largest_table([[1, 0], [0, 1], [3, 4]], [8, 6, 36]))
