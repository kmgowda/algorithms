"""Volume 1, Chapter 20 - Arrays in Depth: Rows, Columns, and Grids.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

SEATS = [[0, 1, 0, 0, 1],
         [1, 0, 1, 1, 0],
         [0, 0, 1, 0, 1]]


def address(r: int, c: int, cols: int, start: int = 1000) -> int:
    """Row-major address of cell (r, c) (Figure 20.2)."""
    return start + r * cols + c


def neighbours(r: int, c: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """The up, down, left and right neighbours of (r, c) that lie inside a rows x cols grid (Figure 20.4)."""
    result = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            result.append((nr, nc))
    return result


def totals(grid: list[list[int]]) -> tuple[list[int], list[int]]:
    """Row and column totals in one walk (Figure 20.5)."""
    rows, cols = len(grid), len(grid[0])
    row_total, col_total = [0] * rows, [0] * cols
    for r in range(rows):
        for c in range(cols):
            row_total[r] += grid[r][c]
            col_total[c] += grid[r][c]
    return row_total, col_total


def lonely_seats(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Taken seats whose neighbours are all free (Exercise 5)."""
    rows, cols = len(grid), len(grid[0])
    return [(r, c) for r in range(rows) for c in range(cols)
            if grid[r][c] and all(grid[nr][nc] == 0 for nr, nc in neighbours(r, c, rows, cols))]


def make_grid(rows: int, cols: int) -> list[list[int]]:
    """A grid whose rows are separate lists (Section 20.9)."""
    return [[0] * cols for _ in range(rows)]


if __name__ == "__main__":
    print(address(1, 3, 5), neighbours(1, 3, 3, 5), neighbours(0, 0, 3, 5), totals(SEATS))
    print(lonely_seats(SEATS))
    bad = [[0] * 5] * 3
    bad[0][0] = 1
    print("shared rows:", [row[0] for row in bad], "separate rows:", [row[0] for row in make_grid(3, 5)])
