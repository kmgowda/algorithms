"""Volume 7, Chapter 25 - Duality and LP Rounding: prices for resources, certificates of optimality, and a
2-approximation for weighted vertex cover by rounding a linear program.

The exact simplex of Chapter 24 is loaded from its own folder, so the two chapters share one implementation.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

import importlib.util
import itertools
from fractions import Fraction
from pathlib import Path

_SIMPLEX = Path(__file__).resolve().parent.parent / "chapter_24_simplex" / "ch24_examples.py"
_spec = importlib.util.spec_from_file_location("ch24_simplex_for_ch25", _SIMPLEX)
sx = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sx)
simplex = sx.simplex

LIBRARY_A, LIBRARY_B, LIBRARY_C = sx.LIBRARY_A, sx.LIBRARY_B, sx.LIBRARY_C

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]
# A warden's daily wage at each place, in tens of pounds.
WAGE = {"Library": 4, "School": 2, "Park": 8, "Market": 1, "Station": 7, "Museum": 7, "Hospital": 1, "Harbour": 8}


def dual(A: list, b: list, c: list) -> tuple[list, list, list]:
    """The dual of max c.x, A x <= b, x >= 0 is min b.y, A^T y >= c, y >= 0; returned in standard form
    (maximise -b.y subject to -A^T y <= -c), so the same simplex solves it."""
    m, n = len(A), len(c)
    At = [[-A[i][j] for i in range(m)] for j in range(n)]
    return At, [-v for v in c], [-v for v in b]


def objective(c: list, x: list):
    return sum(ci * xi for ci, xi in zip(c, x))


def is_certificate(A: list, b: list, c: list, x: list, y: list) -> bool:
    """A plan x and prices y prove each other optimal: both feasible and c.x = b.y."""
    plan_ok = all(v >= 0 for v in x) and all(sum(a * v for a, v in zip(row, x)) <= t for row, t in zip(A, b))
    price_ok = all(v >= 0 for v in y) and all(sum(A[i][j] * y[i] for i in range(len(A))) >= c[j]
                                              for j in range(len(c)))
    return plan_ok and price_ok and objective(c, x) == objective(b, y)


def complementary_slackness(A: list, b: list, c: list, x: list, y: list) -> bool:
    """Unused resource -> price 0; item made -> its prices add up to exactly its value."""
    for i, row in enumerate(A):
        if sum(a * v for a, v in zip(row, x)) < b[i] and y[i] != 0:
            return False
    for j in range(len(c)):
        if x[j] > 0 and sum(A[i][j] * y[i] for i in range(len(A))) != c[j]:
            return False
    return True


def cover_lp(vertices: list, edges: list, cost: dict) -> tuple[Fraction, dict]:
    """Relax weighted vertex cover: minimise sum cost[v] x_v with x_u + x_v >= 1 per road and x >= 0."""
    idx = {v: i for i, v in enumerate(vertices)}
    A, b = [], []
    for u, v in edges:
        row = [0] * len(vertices)
        row[idx[u]] = row[idx[v]] = -1
        A.append(row)
        b.append(-1)
    res = simplex(A, b, [-cost[v] for v in vertices])
    if not edges:
        return Fraction(0), {v: Fraction(0) for v in vertices}
    return -res["value"], dict(zip(vertices, res["x"]))


def round_cover(x: dict) -> list:
    """Keep every place whose LP value is at least one half."""
    return [v for v, xv in x.items() if xv >= Fraction(1, 2)]


def best_weighted_cover(vertices: list, edges: list, cost: dict) -> tuple[int, list]:
    """Exhaustive search, for checking (2^n subsets)."""
    best = None
    for k in range(len(vertices) + 1):
        for g in itertools.combinations(vertices, k):
            if all(a in g or b in g for a, b in edges):
                total = sum(cost[v] for v in g)
                if best is None or total < best[0]:
                    best = (total, list(g))
    return best


def pricing_cover(edges: list, cost: dict) -> tuple[list, dict]:
    """Bar-Yehuda and Even: raise each road's price until one end is fully paid; post wardens at paid ends."""
    paid = {v: Fraction(0) for v in cost}
    price = {}
    for u, v in edges:
        raise_by = min(cost[u] - paid[u], cost[v] - paid[v])
        price[(u, v)] = raise_by
        paid[u] += raise_by
        paid[v] += raise_by
    return [v for v in cost if paid[v] == cost[v] and any(v in e for e in edges)], price


if __name__ == "__main__":
    primal = simplex(LIBRARY_A, LIBRARY_B, LIBRARY_C)
    d = simplex(*dual(LIBRARY_A, LIBRARY_B, LIBRARY_C))
    prices = d["x"]
    print("plan", primal["x"], "loans", primal["value"], "| prices", prices, "cost", -d["value"])
    print("certificate:", is_certificate(LIBRARY_A, LIBRARY_B, LIBRARY_C, primal["x"], prices),
          "complementary slackness:", complementary_slackness(LIBRARY_A, LIBRARY_B, LIBRARY_C, primal["x"], prices))
    lp, x = cover_lp(TOWN, ROADS, WAGE)
    r = round_cover(x)
    print("cover LP", lp, {v: str(t) for v, t in x.items()})
    print("rounded", r, sum(WAGE[v] for v in r), "best", best_weighted_cover(TOWN, ROADS, WAGE))
    print("pricing", pricing_cover(ROADS, WAGE))
