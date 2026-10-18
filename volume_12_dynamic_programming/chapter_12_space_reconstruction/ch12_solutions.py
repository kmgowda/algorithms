"""Volume 12, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations


def lcs_two_rows(a: str, b: str) -> int:
    """Exercise 1: LCS length with O(min(m, n)) memory."""
    if len(a) < len(b):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if a[i - 1] == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def fib_constant_space(n: int) -> int:
    """Exercise 2: Fibonacci with two variables - each value needs only the previous two."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def min_path_with_route(grid: list[list[int]]) -> tuple[int, list[tuple[int, int]]]:
    """Exercise 3: the cheapest right/down walk AND the cells it uses (walk back choosing the cheaper neighbour)."""
    rows, cols = len(grid), len(grid[0])
    c = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for k in range(cols):
            up = c[r - 1][k] if r else None
            left = c[r][k - 1] if k else None
            options = [x for x in (up, left) if x is not None]
            c[r][k] = grid[r][k] + (min(options) if options else 0)
    path, r, k = [(rows - 1, cols - 1)], rows - 1, cols - 1
    while (r, k) != (0, 0):
        if r and (not k or c[r - 1][k] <= c[r][k - 1]):
            r -= 1
        else:
            k -= 1
        path.append((r, k))
    return c[-1][-1], path[::-1]


if __name__ == "__main__":
    print(lcs_two_rows("ACCGGTCG", "GTCGTTCG"), fib_constant_space(90), min_path_with_route([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))
