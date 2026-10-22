"""Volume 6, Chapter 5 - Pruning: cut branches early with feasibility checks, good ordering, and bounds.

Run:  python3 ch05_examples.py
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


# Section 5.6: Saturday's duties, and the volunteer teams that offer to cover them. Each duty must be done by
# exactly one team, so the chosen teams must cover every duty exactly once: an exact cover.
DUTIES = ["Desk", "Shelving", "Storytime", "Displays", "Tea", "Leaflets"]
TEAMS = {"A": ["Desk", "Tea"], "B": ["Shelving", "Storytime"], "C": ["Desk", "Displays"],
         "D": ["Storytime", "Displays", "Tea"], "E": ["Shelving", "Leaflets"], "F": ["Displays", "Leaflets"],
         "G": ["Desk", "Shelving", "Tea"]}


def exact_cover_brute(columns: list, rows: dict) -> list:
    """Try every set of rows (2^rows of them) and keep those that cover each column exactly once."""
    names, out = sorted(rows), []
    for mask in range(1 << len(names)):
        chosen = [names[i] for i in range(len(names)) if mask >> i & 1]
        cells = [c for r in chosen for c in rows[r]]
        if sorted(cells) == sorted(columns):
            out.append(chosen)
    return out


class Node:
    """One 1 of the matrix in Knuth's dancing links: linked left/right in its row, up/down in its column."""
    def __init__(self, column=None, row=None):
        self.left = self.right = self.up = self.down = self
        self.column, self.row = column, row


class Column(Node):
    def __init__(self, name):
        super().__init__()
        self.column, self.name, self.size = self, name, 0


def build_links(columns: list, rows: dict) -> Column:
    """The header, a ring of column headers, and one node for every 1 of the matrix (Figure 5.6)."""
    head = Column("head")
    cols = {}
    for name in columns:
        c = Column(name)
        c.left, c.right = head.left, head
        head.left.right = c
        head.left = c
        cols[name] = c
    for r, cells in rows.items():
        first = None
        for name in cells:
            c = cols[name]
            x = Node(c, r)
            x.up, x.down = c.up, c
            c.up.down = x
            c.up = x
            c.size += 1
            if first is None:
                first = x
            else:
                x.left, x.right = first.left, first
                first.left.right = x
                first.left = x
    return head


def cover(c: Column) -> None:
    """Take column c out of the header ring, and every row that uses c out of the other columns."""
    c.right.left, c.left.right = c.left, c.right
    i = c.down
    while i is not c:
        j = i.right
        while j is not i:
            j.down.up, j.up.down = j.up, j.down
            j.column.size -= 1
            j = j.right
        i = i.down


def uncover(c: Column) -> None:
    """Undo cover(c) exactly, in reverse order: each removed node still remembers its neighbours."""
    i = c.up
    while i is not c:
        j = i.left
        while j is not i:
            j.column.size += 1
            j.down.up = j.up.down = j
            j = j.left
        i = i.up
    c.right.left = c.left.right = c


def algorithm_x(columns: list, rows: dict, log: list | None = None) -> tuple[list, int]:
    """Knuth's Algorithm X with dancing links: every exact cover, and the number of search nodes."""
    head = build_links(columns, rows)
    out, chosen, nodes = [], [], [0]

    def search():
        nodes[0] += 1
        if head.right is head:
            out.append(sorted(chosen))
            return
        c, j = None, head.right
        while j is not head:                          # the column with the fewest 1s left: the hardest duty
            if c is None or j.size < c.size:
                c = j
            j = j.right
        if log is not None:
            log.append((c.name, c.size))
        cover(c)
        r = c.down
        while r is not c:
            chosen.append(r.row)
            j = r.right
            while j is not r:
                cover(j.column)
                j = j.right
            search()
            j = r.left
            while j is not r:
                uncover(j.column)
                j = j.left
            chosen.pop()
            r = r.down
        uncover(c)

    search()
    return out, nodes[0]


def sudoku_rows(grid: list) -> tuple[list, dict]:
    """Sudoku as exact cover: a row for each (cell, digit) allowed by the givens; a column for each rule
    'this cell is filled', 'this row has digit v', 'this column has v', 'this box has v'."""
    n = len(grid)
    box = int(n ** 0.5)
    columns = ([f"cell {r}{c}" for r in range(n) for c in range(n)] + [f"row {r} has {v}" for r in range(n) for v in range(1, n + 1)]
               + [f"col {c} has {v}" for c in range(n) for v in range(1, n + 1)]
               + [f"box {b} has {v}" for b in range(n) for v in range(1, n + 1)])
    rows = {}
    for r in range(n):
        for c in range(n):
            for v in ([grid[r][c]] if grid[r][c] else range(1, n + 1)):
                b = (r // box) * box + c // box
                rows[(r, c, v)] = [f"cell {r}{c}", f"row {r} has {v}", f"col {c} has {v}", f"box {b} has {v}"]
    return columns, rows


def sudoku_exact_cover(grid: list) -> tuple[list | None, int]:
    """Solve a Sudoku by Algorithm X. Returns (grid, search nodes)."""
    columns, rows = sudoku_rows(grid)
    covers, nodes = algorithm_x(columns, rows)
    if not covers:
        return None, nodes
    g = [list(r) for r in grid]
    for r, c, v in covers[0]:
        g[r][c] = v
    return g, nodes


PUZZLE = ["530070000", "600195000", "098000060", "800060003", "400803001", "700020006", "060000280",
          "000419005", "000080079"]
GRID = [[int(ch) for ch in row] for row in PUZZLE]

if __name__ == "__main__":
    for prune in (False, True):
        for s in (False, True):
            print(prune, s, subset_sum(VOUCHERS, TARGET, prune, s))
    print(sudoku(GRID, False)[1], sudoku(GRID, True)[1])
