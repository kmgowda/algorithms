"""Volume 4, Chapter 28 - Puzzles with Rules: N queens and Sudoku by backtracking.

Run:  python3 ch28_examples.py
"""

from __future__ import annotations


def queens(n: int, first_only: bool = False) -> tuple[list, int]:
    """Place n queens, one per row, so that none attack each other (Figure 28.2). Returns (solutions, nodes)."""
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


PUZZLE4 = [[1, 0, 0, 0], [0, 0, 3, 0], [0, 4, 0, 0], [0, 0, 0, 2]]

if __name__ == "__main__":
    for n in (1, 2, 3, 4, 5, 6, 8):
        sols, nodes = queens(n)
        print(n, len(sols), nodes)
    print(queens(8, True))
    print(sudoku(PUZZLE4))
