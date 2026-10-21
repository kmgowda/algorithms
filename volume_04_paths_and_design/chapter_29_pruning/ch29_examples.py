"""Volume 4, Chapter 29 - Pruning: cut branches early with feasibility checks, good ordering, and bounds.

Run:  python3 ch29_examples.py
"""

from __future__ import annotations

# Gift vouchers the club owns; can some of them pay a bill of exactly TARGET pounds?
VOUCHERS = [3, 34, 4, 12, 5, 2, 17, 9, 21, 8]
TARGET = 50


def subset_sum(values: list, target: int, prune: bool, sort_first: bool) -> tuple[list | None, int]:
    """Find vouchers adding to target. prune: stop when the total passes target or the rest cannot reach it.
    Returns (vouchers used, nodes visited)."""
    vals = sorted(values, reverse=True) if sort_first else list(values)
    suffix = [0] * (len(vals) + 1)
    for i in range(len(vals) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + vals[i]
    nodes = [0]

    def go(i, total, chosen):
        nodes[0] += 1
        if total == target:
            return list(chosen)
        if i == len(vals):
            return None
        if prune and (total > target or total + suffix[i] < target):
            return None
        chosen.append(vals[i])
        found = go(i + 1, total + vals[i], chosen)
        chosen.pop()
        return found or go(i + 1, total, chosen)

    return go(0, 0, []), nodes[0]


def sudoku(grid: list, fewest_first: bool) -> tuple[list | None, int]:
    """9 x 9 Sudoku; fewest_first fills the empty cell with the fewest possible digits next."""
    g = [list(r) for r in grid]
    guesses = [0]

    def options(r, c):
        used = set(g[r]) | {g[i][c] for i in range(9)}
        br, bc = r - r % 3, c - c % 3
        used |= {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
        return [v for v in range(1, 10) if v not in used]

    def go():
        empty = [(r, c) for r in range(9) for c in range(9) if g[r][c] == 0]
        if not empty:
            return True
        if fewest_first:
            r, c = min(empty, key=lambda rc: len(options(*rc)))
        else:
            r, c = empty[0]
        for v in options(r, c):
            guesses[0] += 1
            g[r][c] = v
            if go():
                return True
            g[r][c] = 0
        return False

    return (g if go() else None), guesses[0]


PUZZLE = ["530070000", "600195000", "098000060", "800060003", "400803001", "700020006", "060000280",
          "000419005", "000080079"]
GRID = [[int(ch) for ch in row] for row in PUZZLE]

if __name__ == "__main__":
    for prune in (False, True):
        for s in (False, True):
            print(prune, s, subset_sum(VOUCHERS, TARGET, prune, s))
    print(sudoku(GRID, False)[1], sudoku(GRID, True)[1])
