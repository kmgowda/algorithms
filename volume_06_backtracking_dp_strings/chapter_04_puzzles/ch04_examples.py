"""Volume 6, Chapter 4 - Puzzles with Rules: N queens and Sudoku by backtracking.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations


def queens(n: int, first_only: bool = False) -> tuple[list, int]:
    """Place n queens, one per row, so that none attack each other (Figure 4.1). Returns (solutions, nodes)."""
    cols, d1, d2, row, out, nodes = set(), set(), set(), [], [], [0]

    def go(r):
        nodes[0] += 1
        if r == n:
            out.append(list(row))
            return first_only
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue                              # attacked: prune
            cols.add(c); d1.add(r - c); d2.add(r + c); row.append(c)
            if go(r + 1):
                return True
            cols.remove(c); d1.remove(r - c); d2.remove(r + c); row.pop()
        return False

    go(0)
    return out, nodes[0]


def sudoku(grid: list) -> tuple[list | None, int]:
    """Solve a 4 x 4 or 9 x 9 Sudoku (0 = empty) by trying digits in the first empty cell. Returns (grid, guesses)."""
    n = len(grid)
    box = int(n ** 0.5)
    g = [list(r) for r in grid]
    guesses = [0]

    def ok(r, c, v):
        if v in g[r] or any(g[i][c] == v for i in range(n)):
            return False
        br, bc = r - r % box, c - c % box
        return all(g[i][j] != v for i in range(br, br + box) for j in range(bc, bc + box))

    def go():
        for r in range(n):
            for c in range(n):
                if g[r][c] == 0:
                    for v in range(1, n + 1):
                        if ok(r, c, v):
                            guesses[0] += 1
                            g[r][c] = v
                            if go():
                                return True
                            g[r][c] = 0
                    return False
        return True

    for r in range(n):                                # givens that already break a rule: no search needed
        for c in range(n):
            v, g[r][c] = g[r][c], 0
            if v and not ok(r, c, v):
                return None, 0
            g[r][c] = v
    return (g if go() else None), guesses[0]


def queens_bits(n: int) -> tuple[int, int]:
    """N queens with the attacked columns and diagonals kept as bits of three integers (Section 4.4).
    Returns (number of solutions, nodes); the nodes match queens(n)."""
    full, count, nodes = (1 << n) - 1, [0], [0]

    def go(cols, left, right):
        nodes[0] += 1
        if cols == full:
            count[0] += 1
            return
        free = full & ~(cols | left | right)          # squares of this row that nothing attacks
        while free:
            bit = free & -free                        # the lowest free square
            free -= bit
            go(cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1)

    go(0, 0, 0)
    return count[0], nodes[0]


def candidates(g: list, r: int, c: int) -> set:
    n = len(g)
    box = int(n ** 0.5)
    used = set(g[r]) | {g[i][c] for i in range(n)}
    br, bc = r - r % box, c - c % box
    used |= {g[i][j] for i in range(br, br + box) for j in range(bc, bc + box)}
    return set(range(1, n + 1)) - used


def units(n: int) -> list:
    """Every row, column, and box of an n x n grid, as lists of cells."""
    box = int(n ** 0.5)
    rows = [[(r, c) for c in range(n)] for r in range(n)]
    cols = [[(r, c) for r in range(n)] for c in range(n)]
    boxes = [[(br + i, bc + j) for i in range(box) for j in range(box)]
             for br in range(0, n, box) for bc in range(0, n, box)]
    return rows + cols + boxes


def propagate(g: list) -> bool:
    """Fill every forced cell (Figure 4.3) until none is left. A naked single is a cell with one possible digit;
    a hidden single is a digit with only one possible cell in some row, column, or box.
    Returns False if a contradiction appears (a cell with no digit, or a digit with no cell)."""
    n = len(g)
    changed = True
    while changed:
        changed = False
        for r in range(n):
            for c in range(n):
                if g[r][c] == 0:
                    opts = candidates(g, r, c)
                    if not opts:
                        return False
                    if len(opts) == 1:
                        g[r][c] = opts.pop()          # naked single
                        changed = True
        for unit in units(n):
            for v in range(1, n + 1):
                if any(g[r][c] == v for r, c in unit):
                    continue
                spots = [(r, c) for r, c in unit if g[r][c] == 0 and v in candidates(g, r, c)]
                if not spots:
                    return False
                if len(spots) == 1:
                    r, c = spots[0]
                    g[r][c] = v                       # hidden single
                    changed = True
    return True


def sudoku_propagate(grid: list) -> tuple[list | None, int]:
    """Backtracking that propagates forced cells after every guess and guesses in the cell with the fewest options.
    Returns (solved grid, guesses)."""
    n = len(grid)
    guesses = [0]

    def go(g):
        if not propagate(g):
            return None
        empty = [(r, c) for r in range(n) for c in range(n) if g[r][c] == 0]
        if not empty:
            return g
        r, c = min(empty, key=lambda rc: len(candidates(g, *rc)))
        for v in sorted(candidates(g, r, c)):
            guesses[0] += 1
            h = [list(row) for row in g]
            h[r][c] = v
            done = go(h)
            if done:
                return done
        return None

    for r in range(n):                                # givens that already break a rule
        for c in range(n):
            v = grid[r][c]
            if v:
                g = [list(row) for row in grid]
                g[r][c] = 0
                if v not in candidates(g, r, c):
                    return None, 0
    return go([list(row) for row in grid]), guesses[0]


PUZZLE4 = [[1, 0, 0, 0], [0, 0, 3, 0], [0, 4, 0, 0], [0, 0, 0, 2]]
CLASSIC = [[int(ch) for ch in row] for row in ["530070000", "600195000", "098000060", "800060003", "400803001",
                                                 "700020006", "060000280", "000419005", "000080079"]]
HARD = [[int(ch) for ch in row] for row in ["800000000", "003600000", "070090200", "050007000", "000045700",
                                              "000100030", "001000068", "008500010", "090000400"]]

if __name__ == "__main__":
    for n in (1, 2, 3, 4, 5, 6, 8):
        sols, nodes = queens(n)
        print(n, len(sols), nodes)
    print(queens(8, True))
    print(sudoku(PUZZLE4))
