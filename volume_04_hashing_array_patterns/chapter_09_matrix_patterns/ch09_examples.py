"""Volume 4, Chapter 9 - Matrix Patterns: 2-D Prefix Sums, Diagonals, In-Place Rotation, Search.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

Grid = list[list[int]]


class RectangleTotals:
    """LeetCode 304: total of any rectangle in O(1) after O(rows x cols) setup.

    P[r][c] = total of the rectangle from (0, 0) up to but not including (r, c).
    """

    def __init__(self, grid: Grid) -> None:
        rows, cols = len(grid), len(grid[0]) if grid else 0
        self.P = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self.P[r + 1][c + 1] = grid[r][c] + self.P[r][c + 1] + self.P[r + 1][c] - self.P[r][c]

    def total(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Inclusive corners (r1, c1) top-left to (r2, c2) bottom-right."""
        P = self.P
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]


def densest_square(grid: Grid, k: int) -> tuple[int, int, int]:
    """Industry example: the k x k field area with the most crops (or brightest image patch). (row, col, total)."""
    rt = RectangleTotals(grid)
    best = (0, 0, rt.total(0, 0, k - 1, k - 1))
    for r in range(len(grid) - k + 1):
        for c in range(len(grid[0]) - k + 1):
            t = rt.total(r, c, r + k - 1, c + k - 1)
            if t > best[2]:
                best = (r, c, t)
    return best


def is_toeplitz(grid: Grid) -> bool:
    """LeetCode 766: every top-left to bottom-right diagonal is constant. Cells on one diagonal share r - c."""
    first_on_diagonal: dict[int, int] = {}
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if first_on_diagonal.setdefault(r - c, v) != v:
                return False
    return True


def zigzag_diagonals(grid: Grid) -> list[int]:
    """LeetCode 498: walk anti-diagonals (cells sharing r + c), alternating direction."""
    if not grid:
        return []
    rows, cols = len(grid), len(grid[0])
    out: list[int] = []
    for d in range(rows + cols - 1):
        cells = [grid[r][d - r] for r in range(max(0, d - cols + 1), min(rows, d + 1))]
        out.extend(cells[::-1] if d % 2 == 0 else cells)
    return out


def rotate_in_place(grid: Grid) -> None:
    """LeetCode 48: rotate a square grid 90 degrees clockwise using O(1) extra space - four-way swaps per ring."""
    n = len(grid)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = grid[first][i]
            grid[first][i] = grid[last - offset][first]          # left -> top
            grid[last - offset][first] = grid[last][last - offset]  # bottom -> left
            grid[last][last - offset] = grid[i][last]            # right -> bottom
            grid[i][last] = top                                  # top -> right


def search_row_sorted(grid: Grid, target: int) -> bool:
    """LeetCode 74: rows sorted and each row starts after the previous ends - binary search as one long list."""
    if not grid or not grid[0]:
        return False
    cols = len(grid[0])
    low, high = 0, len(grid) * cols - 1
    while low <= high:
        mid = (low + high) // 2
        value = grid[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return False


if __name__ == "__main__":
    field = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1], [4, 1, 0, 5]]
    rt = RectangleTotals(field)
    print("Rows 1-2, cols 1-3 total:", rt.total(1, 1, 2, 3), "| densest 2x2:", densest_square(field, 2))
    print("Toeplitz?", is_toeplitz([[1, 2, 3], [4, 1, 2], [5, 4, 1]]))
    print("Zigzag:", zigzag_diagonals([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_in_place(g)
    print("Rotated:", g, "| search 16:", search_row_sorted([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 16))
