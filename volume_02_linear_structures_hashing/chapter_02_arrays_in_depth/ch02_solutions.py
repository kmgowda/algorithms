"""Volume 2, Chapter 2 - Thinking Problems.

Problem 1: the most taken seats a grid can hold when every taken seat is lonely (checked by brute force).
Problem 2: turn a square grid a quarter turn clockwise in place, with O(1) extra memory.
Problem 3: the neighbour test that forgets `0 <=`, kept here so the tests can show it fails.
"""

from __future__ import annotations

from itertools import product

from ch02_examples import SEATS, lonely_seats


def most_all_lonely(rows: int, cols: int) -> int:
    """Brute force: the largest number of taken seats with every taken seat lonely (small grids only)."""
    best = 0
    for bits in product((0, 1), repeat=rows * cols):
        grid = [list(bits[r * cols:(r + 1) * cols]) for r in range(rows)]
        if len(lonely_seats(grid)) == sum(bits):
            best = max(best, sum(bits))
    return best


def rotate_clockwise(grid: list[list[int]]) -> None:
    """Turn an n x n grid a quarter turn clockwise in place: transpose, then reverse each row."""
    n = len(grid)
    for r in range(n):
        for c in range(r + 1, n):
            grid[r][c], grid[c][r] = grid[c][r], grid[r][c]
    for row in grid:
        row.reverse()


def lonely_seats_no_lower_check(grid: list[list[int]]) -> list[tuple[int, int]]:
    """WRONG: tests only nr < rows and nc < cols, so index -1 silently reads the far edge."""
    rows, cols = len(grid), len(grid[0])
    result = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] and all(grid[r + dr][c + dc] == 0
                                  for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
                                  if r + dr < rows and c + dc < cols):
                result.append((r, c))
    return result


if __name__ == "__main__":
    print([most_all_lonely(r, c) for r, c in ((1, 1), (2, 2), (2, 3), (3, 3))])
    g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_clockwise(g)
    print(g)
    print(lonely_seats(SEATS), lonely_seats_no_lower_check(SEATS))
