"""Volume 7, Chapter 24 - The Simplex Method: walk from corner to better corner, exactly, with fractions.

Every linear program here is in standard form: maximise c.x subject to A x <= b and x >= 0.
The tableau has one row per constraint and a last row for the objective:

    row i:      a_i1 ... a_in  s_1 ... s_m | b_i         (s_i is the slack of constraint i)
    last row:   c_1  ... c_n   0   ...  0  | 0           (reduced costs; the corner's value is minus the last entry)

A positive entry in the last row means "increasing this variable still pays".

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

from fractions import Fraction

# Maya's reading room (Chapter 23): x hardbacks, y paperbacks; loans 3x + 2y.
LIBRARY_A = [[2, 1],      # money, in tens of pounds: 20x + 10y <= 800
             [1, 1],      # display slots:            x + y <= 50
             [1, 3]]      # cataloguing, 10-minute units: x + 3y <= 120
LIBRARY_B = [80, 50, 120]
LIBRARY_C = [3, 2]

# Chvatal's example (Linear Programming, 1983, p. 31): the largest-coefficient rule cycles at a degenerate corner.
CYCLING_A = [[Fraction(1, 2), Fraction(-11, 2), Fraction(-5, 2), 9],
             [Fraction(1, 2), Fraction(-3, 2), Fraction(-1, 2), 1],
             [1, 0, 0, 0]]
CYCLING_B = [0, 0, 1]
CYCLING_C = [10, -57, -9, -24]


def tableau(A: list, b: list, c: list) -> tuple[list, list]:
    """The starting tableau with a slack variable per row; the slacks form the first basis."""
    m, n = len(A), len(c)
    T = []
    for i in range(m):
        slack = [Fraction(int(i == j)) for j in range(m)]
        T.append([Fraction(v) for v in A[i]] + slack + [Fraction(b[i])])
    T.append([Fraction(v) for v in c] + [Fraction(0)] * m + [Fraction(0)])
    return T, list(range(n, n + m))


def pivot(T: list, basis: list, r: int, k: int) -> None:
    """Make column k basic in row r: scale row r so the pivot is 1, then clear column k from every other row."""
    p = T[r][k]
    T[r] = [v / p for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][k] != 0:
            f = T[i][k]
            T[i] = [a - f * e for a, e in zip(T[i], T[r])]
    basis[r] = k


def entering(T: list, rule: str = "bland"):
    """A column whose reduced cost is positive: the smallest index (Bland) or the largest cost (Dantzig)."""
    obj = T[-1][:-1]
    candidates = [k for k, v in enumerate(obj) if v > 0]
    if not candidates:
        return None
    if rule == "bland":
        return candidates[0]
    return max(candidates, key=lambda k: (obj[k], -k))


def leaving(T: list, basis: list, k: int):
    """The ratio test: the row that stops column k first; ties go to the smallest basic variable."""
    rows = [i for i in range(len(T) - 1) if T[i][k] > 0]
    if not rows:
        return None
    return min(rows, key=lambda i: (T[i][-1] / T[i][k], basis[i]))


def run(T: list, basis: list, rule: str = "bland", trace=None, limit: int = 10_000) -> str:
    """Pivot until no column pays ('optimal'), a column is unlimited ('unbounded'), or a basis repeats ('cycling')."""
    seen = {tuple(basis)}
    for _ in range(limit):
        k = entering(T, rule)
        if k is None:
            return "optimal"
        r = leaving(T, basis, k)
        if r is None:
            return "unbounded"
        if trace is not None:
            trace.append((k, basis[r], T[r][-1] / T[r][k]))
        pivot(T, basis, r, k)
        if tuple(basis) in seen:
            return "cycling"
        seen.add(tuple(basis))
    return "limit"


def phase_one(T: list, basis: list, n: int, trace=None):
    """Origin infeasible: add x0, subtract it from every row, and minimise it. Returns the tableau without x0, or None."""
    m = len(T) - 1
    goal = T[-1]
    aux = [row[:-1] + [Fraction(-1)] + row[-1:] for row in T[:-1]]
    aux.append([Fraction(0)] * (len(goal) - 1) + [Fraction(-1), Fraction(0)])
    x0 = len(goal) - 1
    r = min(range(m), key=lambda i: aux[i][-1])
    if trace is not None:
        trace.append((x0, basis[r], -aux[r][-1]))
    pivot(aux, basis, r, x0)
    run(aux, basis, "bland", trace)
    if aux[-1][-1] != 0:          # the least possible x0 is above zero: no plan obeys every rule
        return None
    if x0 in basis:               # x0 = 0 but still basic: swap it out for any column with a non-zero entry
        r = basis.index(x0)
        k = next(j for j in range(x0) if aux[r][j] != 0)
        pivot(aux, basis, r, k)
    T2 = [row[:x0] + row[x0 + 1:] for row in aux[:-1]]
    obj = goal[:]
    for i, j in enumerate(basis):
        if obj[j] != 0:
            f = obj[j]
            obj = [a - f * e for a, e in zip(obj, T2[i])]
    T2.append(obj)
    return T2


def simplex(A: list, b: list, c: list, rule: str = "bland", trace=None) -> dict:
    """Maximise c.x subject to A x <= b, x >= 0, exactly. Returns status, x, value, duals (shadow prices), pivots."""
    m, n = len(A), len(c)
    T, basis = tableau(A, b, c)
    steps = [] if trace is None else trace
    if any(v < 0 for v in b):
        T = phase_one(T, basis, n, steps)
        if T is None:
            return {"status": "infeasible", "pivots": len(steps)}
    status = run(T, basis, rule, steps)
    out = {"status": status, "pivots": len(steps), "basis": basis[:], "tableau": T}
    if status == "optimal":
        x = [Fraction(0)] * (n + m)
        for i, j in enumerate(basis):
            x[j] = T[i][-1]
        out.update(x=x[:n], slack=x[n:], value=-T[-1][-1], duals=[-T[-1][n + i] for i in range(m)])
    return out


def klee_minty(n: int) -> tuple[list, list, list]:
    """Klee and Minty's squashed cube (CLRS form): Dantzig's rule visits all 2^n corners."""
    A = [[2 ** (i - j + 1) if j < i else int(i == j) for j in range(n)] for i in range(n)]
    b = [5 ** (i + 1) for i in range(n)]
    c = [2 ** (n - 1 - j) for j in range(n)]
    return A, b, c


def corners_walked(A: list, b: list, c: list, rule: str = "bland") -> list:
    """The corners (values of the original variables) visited, from the origin to the end."""
    T, basis = tableau(A, b, c)
    n = len(c)
    path = []

    def where():
        x = [Fraction(0)] * len(T[0][:-1])
        for i, j in enumerate(basis):
            x[j] = T[i][-1]
        return tuple(x[:n])

    path.append(where())
    while (k := entering(T, rule)) is not None and (r := leaving(T, basis, k)) is not None:
        pivot(T, basis, r, k)
        path.append(where())
    return path


def show(T: list, basis: list, names: list) -> str:
    """A tableau as text, for reading a trace."""
    lines = ["basis | " + " ".join(f"{s:>6}" for s in names) + " |    rhs"]
    for i, row in enumerate(T[:-1]):
        lines.append(f"{names[basis[i]]:>5} | " + " ".join(f"{str(v):>6}" for v in row[:-1]) + f" | {str(row[-1]):>6}")
    lines.append("    z | " + " ".join(f"{str(v):>6}" for v in T[-1][:-1]) + f" | {str(-T[-1][-1]):>6}")
    return "\n".join(lines)


if __name__ == "__main__":
    steps = []
    res = simplex(LIBRARY_A, LIBRARY_B, LIBRARY_C, trace=steps)
    print("library:", res["status"], [str(v) for v in res["x"]], "loans", res["value"],
          "duals", [str(v) for v in res["duals"]], "pivots", steps)
    print("corners walked:", corners_walked(LIBRARY_A, LIBRARY_B, LIBRARY_C))
    T, basis = tableau(CYCLING_A, CYCLING_B, CYCLING_C)
    print("Chvatal, largest coefficient:", run(T, basis, "largest"))
    print("Chvatal, Bland:", simplex(CYCLING_A, CYCLING_B, CYCLING_C)["value"])
    for n in range(1, 7):
        km = simplex(*klee_minty(n), rule="largest")
        print("Klee-Minty", n, "pivots", km["pivots"], "value", km["value"])
