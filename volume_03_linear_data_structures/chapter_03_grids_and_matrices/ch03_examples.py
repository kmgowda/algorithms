"""Volume 3, Chapter 3 - Two-Dimensional Arrays: Grids, Seats, Images, and Matrices.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator

Grid = list[list[Any]]


def make_grid(rows: int, cols: int, fill: Any = 0) -> Grid:
    """A rows x cols grid where every row is its OWN list (avoids the [[0]*c]*r trap)."""
    return [[fill] * cols for _ in range(rows)]


class FlatGrid:
    """A grid stored in ONE flat list, row after row ("row-major order"): cell (r, c) is at r*cols + c."""

    def __init__(self, rows: int, cols: int, fill: Any = 0) -> None:
        if rows < 1 or cols < 1:
            raise ValueError("grid needs at least one row and column")
        self.rows, self.cols = rows, cols
        self._cells = [fill] * (rows * cols)

    def _offset(self, r: int, c: int) -> int:
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise IndexError(f"cell ({r}, {c}) is outside the grid")
        return r * self.cols + c

    def __getitem__(self, position: tuple[int, int]) -> Any:
        return self._cells[self._offset(*position)]

    def __setitem__(self, position: tuple[int, int], value: Any) -> None:
        self._cells[self._offset(*position)] = value

    def to_rows(self) -> Grid:
        return [self._cells[r * self.cols:(r + 1) * self.cols] for r in range(self.rows)]


def neighbors(grid: Grid, r: int, c: int) -> Iterator[tuple[int, int]]:
    """The up/down/left/right neighbours that exist (no stepping off the edge)."""
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


def transpose(grid: Grid) -> Grid:
    """Rows become columns."""
    return [[grid[r][c] for r in range(len(grid))] for c in range(len(grid[0]))]


def rotate_clockwise(grid: Grid) -> Grid:
    """Rotate 90 degrees clockwise = transpose, then reverse each row."""
    return [row[::-1] for row in transpose(grid)]


def spiral_order(grid: Grid) -> list[Any]:
    """Walk the outside ring clockwise, then the next ring in, and so on (LeetCode 54)."""
    result: list[Any] = []
    if not grid:
        return result
    top, bottom, left, right = 0, len(grid) - 1, 0, len(grid[0]) - 1
    while top <= bottom and left <= right:
        result.extend(grid[top][c] for c in range(left, right + 1))
        result.extend(grid[r][right] for r in range(top + 1, bottom + 1))
        if top < bottom:
            result.extend(grid[bottom][c] for c in range(right - 1, left - 1, -1))
        if left < right:
            result.extend(grid[r][left] for r in range(bottom - 1, top, -1))
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return result


def best_free_seat(seats: Grid) -> tuple[int, int] | None:
    """Practical example: the free seat (value 0) closest to the screen's centre in the middle row."""
    centre_r, centre_c = len(seats) / 2, (len(seats[0]) - 1) / 2
    best, best_distance = None, float("inf")
    for r, row in enumerate(seats):
        for c, taken in enumerate(row):
            if not taken:
                distance = abs(r - centre_r) + abs(c - centre_c)
                if distance < best_distance:
                    best, best_distance = (r, c), distance
    return best


def box_blur(image: Grid) -> Grid:
    """Industry example: soften a grayscale image - each pixel becomes the average of itself and its neighbours."""
    blurred = make_grid(len(image), len(image[0]))
    for r in range(len(image)):
        for c in range(len(image[0])):
            cells = [(r, c), *neighbors(image, r, c)]
            blurred[r][c] = round(sum(image[i][j] for i, j in cells) / len(cells))
    return blurred


def matrix_multiply(a: Grid, b: Grid) -> Grid:
    """Industry example: graphics and machine learning multiply matrices constantly. O(n^3) for n x n."""
    if len(a[0]) != len(b):
        raise ValueError("columns of a must equal rows of b")
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


if __name__ == "__main__":
    broken = [[0] * 3] * 2
    broken[0][0] = 9
    print("The aliasing trap:", broken, "| make_grid is safe:", make_grid(2, 3))
    g = FlatGrid(2, 3)
    g[1, 2] = "X"
    print("FlatGrid rows:", g.to_rows())
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Transpose:", transpose(board), "| rotate:", rotate_clockwise(board))
    print("Spiral:", spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
    print("Neighbours of (0, 0):", list(neighbors(board, 0, 0)))
    cinema = [[1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 0, 1], [0, 0, 0, 0, 0]]
    print("Best free seat:", best_free_seat(cinema))
    print("Blur:", box_blur([[0, 0, 0], [0, 255, 0], [0, 0, 0]]))
    print("Scale the point (3, 4) by 2:", matrix_multiply([[2, 0], [0, 2]], [[3], [4]]))
