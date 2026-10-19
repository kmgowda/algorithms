"""Volume 15, Chapter 9 - Linear Programming (Intuition).

Maximise a linear objective subject to linear inequalities. The best point is always at a CORNER of the
feasible region - the key fact behind every LP method.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import itertools
from fractions import Fraction

Constraint = tuple[Fraction, Fraction, Fraction]     # a*x + b*y <= c


def corners(constraints: list[Constraint]) -> list[tuple[Fraction, Fraction]]:
    """Intersect every pair of constraint lines; keep points satisfying all constraints (exact fractions)."""
    pts = []
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(constraints, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue                                         # parallel lines
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if all(a * x + b * y <= c for a, b, c in constraints):
            pts.append((x, y))
    return sorted(set(pts))


def solve_2d(objective: tuple[int, int], constraints: list[tuple[int, int, int]]) -> tuple[Fraction, tuple[Fraction, Fraction]] | None:
    """Maximise p*x + q*y over a bounded 2-variable LP by checking every corner."""
    cons = [(Fraction(a), Fraction(b), Fraction(c)) for a, b, c in constraints]
    pts = corners(cons)
    if not pts:
        return None
    p, q = objective
    best = max(pts, key=lambda pt: p * pt[0] + q * pt[1])
    return p * best[0] + q * best[1], best


def simplex(c: list[float], a: list[list[float]], b: list[float]) -> tuple[float, list[float]]:
    """Maximise c.x subject to A x <= b, x >= 0, with b >= 0 (so x = 0 is a valid start). Tableau simplex:
    walk from corner to neighbouring corner, always improving the objective, until no improvement is left.
    Bland's rule (smallest index) prevents cycling."""
    m, n = len(a), len(c)
    table = [row[:] + [1.0 if i == j else 0.0 for j in range(m)] + [b[i]] for i, row in enumerate(a)]
    obj = [-x for x in c] + [0.0] * m + [0.0]
    basis = [n + i for i in range(m)]
    while True:
        col = next((j for j in range(n + m) if obj[j] < -1e-12), None)
        if col is None:
            break                                            # optimal: no improving direction
        ratios = [(table[i][-1] / table[i][col], basis[i], i) for i in range(m) if table[i][col] > 1e-12]
        if not ratios:
            raise ValueError("unbounded")
        _, _, row = min(ratios)
        piv = table[row][col]
        table[row] = [v / piv for v in table[row]]
        for i in range(m):
            if i != row and abs(table[i][col]) > 1e-12:
                f = table[i][col]
                table[i] = [v - f * w for v, w in zip(table[i], table[row])]
        f = obj[col]
        obj = [v - f * w for v, w in zip(obj, table[row])]
        basis[row] = col
    x = [0.0] * n
    for i, var in enumerate(basis):
        if var < n:
            x[var] = table[i][-1]
    return obj[-1], x


def factory_plan() -> tuple[Fraction, tuple[Fraction, Fraction]] | None:
    """Industry example: chairs earn 30, tables 50. Each chair needs 1 h carpentry + 2 h finishing; each table
    3 h carpentry + 1 h finishing. 90 h carpentry and 80 h finishing are available. Maximise profit."""
    return solve_2d((30, 50), [(1, 3, 90), (2, 1, 80), (-1, 0, 0), (0, -1, 0)])


if __name__ == "__main__":
    print("factory:", factory_plan())
    print("corners:", corners([(Fraction(1), Fraction(3), Fraction(90)), (Fraction(2), Fraction(1), Fraction(80)),
                              (Fraction(-1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(-1), Fraction(0))]))
    print("simplex:", simplex([30, 50], [[1, 3], [2, 1]], [90, 80]))
    print("3 products:", simplex([3, 2, 4], [[1, 1, 2], [2, 1, 3], [2, 2, 1]], [4, 5, 7]))
