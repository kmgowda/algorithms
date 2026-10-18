"""Volume 4, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from ch09_examples import Grid, RectangleTotals


def block_sums(grid: Grid, k: int) -> Grid:
    """Exercise 1 (LeetCode 1314): each cell becomes the total of the (2k+1) x (2k+1) block around it (clipped)."""
    rows, cols = len(grid), len(grid[0])
    rt = RectangleTotals(grid)
    return [[rt.total(max(0, r - k), max(0, c - k), min(rows - 1, r + k), min(cols - 1, c + k))
             for c in range(cols)] for r in range(rows)]


def anti_diagonal_groups(grid: Grid) -> dict[int, list[int]]:
    """Exercise 2: group values by r + c (the anti-diagonals), top row first."""
    groups: dict[int, list[int]] = {}
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            groups.setdefault(r + c, []).append(v)
    return groups


def transpose_in_place(grid: Grid) -> None:
    """Exercise 3: swap across the main diagonal (square grids only)."""
    n = len(grid)
    for r in range(n):
        for c in range(r + 1, n):
            grid[r][c], grid[c][r] = grid[c][r], grid[r][c]


def count_bright_squares(grid: Grid, k: int, threshold: int) -> int:
    """Exercise 4: how many k x k squares have total >= threshold?"""
    rt = RectangleTotals(grid)
    return sum(1 for r in range(len(grid) - k + 1) for c in range(len(grid[0]) - k + 1)
               if rt.total(r, c, r + k - 1, c + k - 1) >= threshold)


if __name__ == "__main__":
    print(block_sums([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1))
    print(anti_diagonal_groups([[1, 2], [3, 4]]))
    g = [[1, 2], [3, 4]]
    transpose_in_place(g)
    print(g, count_bright_squares([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 16))
