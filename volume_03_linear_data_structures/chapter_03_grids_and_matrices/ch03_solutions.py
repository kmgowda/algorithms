"""Volume 3, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any

from ch03_examples import Grid, neighbors


def row_and_column_totals(sales: Grid) -> tuple[list[int], list[int]]:
    """Exercise 1: shop sales grid (rows = shops, columns = days)."""
    rows = [sum(row) for row in sales]
    cols = [sum(sales[r][c] for r in range(len(sales))) for c in range(len(sales[0]))]
    return rows, cols


def mirror_image(image: Grid) -> Grid:
    """Exercise 2 (LeetCode 832 idea): flip each row left-to-right."""
    return [row[::-1] for row in image]


def set_zeroes(grid: Grid) -> None:
    """Exercise 3 (LeetCode 73): if a cell is 0, zero its whole row and column. Two passes, in place."""
    zero_rows = {r for r, row in enumerate(grid) for value in row if value == 0}
    zero_cols = {c for row in grid for c, value in enumerate(row) if value == 0}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if r in zero_rows or c in zero_cols:
                grid[r][c] = 0


def search_sorted_matrix(grid: Grid, target: Any) -> bool:
    """Exercise 4 (LeetCode 240): rows and columns sorted ascending. Start top-right; O(rows + cols)."""
    if not grid:
        return False
    r, c = 0, len(grid[0]) - 1
    while r < len(grid) and c >= 0:
        value = grid[r][c]
        if value == target:
            return True
        if value > target:
            c -= 1            # everything below in this column is even bigger
        else:
            r += 1            # everything left in this row is even smaller
    return False


def life_step(board: Grid) -> Grid:
    """Exercise 5 (LeetCode 289 idea): one step of Conway's Game of Life with 8 neighbours."""
    rows, cols = len(board), len(board[0])
    nxt = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            alive = sum(board[i][j] for i in range(max(0, r - 1), min(rows, r + 2))
                        for j in range(max(0, c - 1), min(cols, c + 2)) if (i, j) != (r, c))
            nxt[r][c] = 1 if alive == 3 or (board[r][c] and alive == 2) else 0
    return nxt


def count_edge_cells(grid: Grid) -> int:
    """Exercise 6: cells with fewer than 4 neighbours lie on the border."""
    return sum(1 for r in range(len(grid)) for c in range(len(grid[0])) if len(list(neighbors(grid, r, c))) < 4)


if __name__ == "__main__":
    print(row_and_column_totals([[5, 3], [2, 7]]), mirror_image([[1, 0, 0]]))
    g = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    set_zeroes(g)
    print(g, search_sorted_matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]], 5))
    print(life_step([[0, 1, 0], [0, 1, 0], [0, 1, 0]]), count_edge_cells([[0] * 4 for _ in range(3)]))
