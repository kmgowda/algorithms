"""Volume 7, Chapter 23 - Linear Programs and Their Corners: the feasible polygon, the best corner, integer plans.

A linear program in standard form: maximise c.x subject to A x <= b and x >= 0. Every computation is exact
(fractions.Fraction), so a corner such as (30, 20) is never printed as 29.999999.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations

import itertools
from fractions import Fraction

# Maya's reading room: x hardbacks, y paperbacks; loans per month 3x + 2y.
LIBRARY_A = [[2, 1],      # money, in tens of pounds: 20x + 10y <= 800
             [1, 1],      # display slots:            x + y <= 50
             [1, 3]]      # cataloguing, 10-minute units: x + 3y <= 120
LIBRARY_B = [80, 50, 120]
LIBRARY_C = [3, 2]
RULES = ["money", "slots", "cataloguing"]

# Whole bookcases only: tall x, low y; loans 5x + 4y; money 6x + 4y <= 24 (hundreds of pounds); floor x + 2y <= 6.
CASES_A = [[6, 4], [1, 2]]
CASES_B = [24, 6]
CASES_C = [5, 4]


def solve(M: list, v: list):
    """Solve the square system M z = v exactly by Gauss-Jordan elimination; None if it has no single solution."""
    n = len(v)
    R = [[Fraction(a) for a in row] + [Fraction(t)] for row, t in zip(M, v)]
    for col in range(n):
        p = next((r for r in range(col, n) if R[r][col] != 0), None)
        if p is None:
            return None
        R[col], R[p] = R[p], R[col]
        R[col] = [a / R[col][col] for a in R[col]]
        for r in range(n):
            if r != col and R[r][col] != 0:
                f = R[r][col]
                R[r] = [a - f * e for a, e in zip(R[r], R[col])]
    return [R[r][n] for r in range(n)]


def feasible(A: list, b: list, x: list) -> bool:
    """Does the plan x obey every rule and stay non-negative?"""
    return all(v >= 0 for v in x) and all(sum(a * v for a, v in zip(row, x)) <= t for row, t in zip(A, b))


def corners(A: list, b: list) -> list:
    """Every corner of {A x <= b, x >= 0}: choose n of the m + n boundary lines, solve, keep the feasible points."""
    n = len(A[0]) if A else 0
    lines = [(row, t) for row, t in zip(A, b)] + [([int(i == j) for j in range(n)], 0) for i in range(n)]
    found = []
    for pick in itertools.combinations(lines, n):
        x = solve([row for row, _ in pick], [t for _, t in pick])
        if x is not None and feasible(A, b, x) and x not in found:
            found.append(x)
    return found


def best_corner(A: list, b: list, c: list):
    """Try every corner and keep the one with the largest objective (assumes the program has a best answer)."""
    best = None
    for x in corners(A, b):
        value = sum(ci * xi for ci, xi in zip(c, x))
        if best is None or value > best[0]:
            best = (value, x)
    return best


def slacks(A: list, b: list, x: list) -> list:
    """How much of each resource a plan leaves unused."""
    return [t - sum(a * v for a, v in zip(row, x)) for row, t in zip(A, b)]


def tight(A: list, b: list, x: list) -> list:
    """The rules a plan meets exactly (slack zero), by index."""
    return [i for i, s in enumerate(slacks(A, b, x)) if s == 0]


def to_standard_form(c: list, rules: list, minimise: bool = False, free: tuple = ()) -> tuple[list, list, list]:
    """Rewrite rules (coefficients, sense, bound) with sense '<=', '>=' or '=' as maximise c.x, A x <= b, x >= 0.
    A '>=' rule is multiplied by -1; an '=' rule becomes two; a free variable v becomes v+ - v-."""
    sign = -1 if minimise else 1
    split = lambda row: [w for j, a in enumerate(row) for w in ((a, -a) if j in free else (a,))]  # noqa: E731
    cc = [sign * w for w in split(c)]
    A, b = [], []
    for row, sense, bound in rules:
        r = split(row)
        if sense in ("<=", "="):
            A.append(r)
            b.append(bound)
        if sense in (">=", "="):
            A.append([-a for a in r])
            b.append(-bound)
    return A, b, cc


def best_integer_plan(A: list, b: list, c: list, top: int):
    """Exhaustive search over whole-number plans 0..top in every coordinate (small programs only)."""
    best = None
    for x in itertools.product(range(top + 1), repeat=len(c)):
        if feasible(A, b, x):
            value = sum(ci * xi for ci, xi in zip(c, x))
            if best is None or value > best[0]:
                best = (value, list(x))
    return best


def cover_as_ip(vertices: list, edges: list, k: int) -> tuple[list, list]:
    """Vertex cover of size <= k as 0-1 integer program rules A x <= b: x_u + x_v >= 1 per road, sum x <= k."""
    idx = {v: i for i, v in enumerate(vertices)}
    A, b = [], []
    for u, v in edges:
        row = [0] * len(vertices)
        row[idx[u]] = row[idx[v]] = -1
        A.append(row)
        b.append(-1)
    A.append([1] * len(vertices))
    b.append(k)
    return A, b


def zero_one_feasible(A: list, b: list, n: int):
    """Try all 2^n plans of 0s and 1s: a plan obeying every rule, or None (exponential: the point of NP-hardness)."""
    for x in itertools.product((0, 1), repeat=n):
        if feasible(A, b, x):
            return list(x)
    return None


if __name__ == "__main__":
    print("corners:", [[str(v) for v in x] for x in corners(LIBRARY_A, LIBRARY_B)])
    value, x = best_corner(LIBRARY_A, LIBRARY_B, LIBRARY_C)
    print("best corner:", x, "loans", value, "slack", slacks(LIBRARY_A, LIBRARY_B, x))
    lp = best_corner(CASES_A, CASES_B, CASES_C)
    print("bookcases LP:", [str(v) for v in lp[1]], lp[0], " integer:", best_integer_plan(CASES_A, CASES_B, CASES_C, 6))
