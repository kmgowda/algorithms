"""Volume 12, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations


def largest_square(grid: list[str]) -> int:
    """Exercise 1 (LeetCode 221): side of the largest all-'1' square.
    s[r][c] = 1 + min(up, left, up-left) when the cell is '1'."""
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    s = [[0] * (cols + 1) for _ in range(rows + 1)]
    best = 0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if grid[r - 1][c - 1] == "1":
                s[r][c] = 1 + min(s[r - 1][c], s[r][c - 1], s[r - 1][c - 1])
                best = max(best, s[r][c])
    return best


def longest_common_substring(a: str, b: str) -> str:
    """Exercise 2: longest CONTIGUOUS common piece - reset to 0 on a mismatch (unlike LCS)."""
    best_len, best_end = 0, 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best_len:
                    best_len, best_end = cur[j], i
        prev = cur
    return a[best_end - best_len:best_end]


def falling_path_min(matrix: list[list[int]]) -> int:
    """Exercise 3 (LeetCode 931): cheapest path from top to bottom, moving straight down or diagonally."""
    prev = list(matrix[0])
    n = len(prev)
    for row in matrix[1:]:
        prev = [row[c] + min(prev[max(0, c - 1):min(n, c + 2)]) for c in range(n)]
    return min(prev)


def is_interleaving(a: str, b: str, c: str) -> bool:
    """Exercise 4 (LeetCode 97): can c be formed by merging a and b while keeping each one's order?"""
    if len(a) + len(b) != len(c):
        return False
    ok = [[False] * (len(b) + 1) for _ in range(len(a) + 1)]
    ok[0][0] = True
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i and a[i - 1] == c[i + j - 1] and ok[i - 1][j]:
                ok[i][j] = True
            if j and b[j - 1] == c[i + j - 1] and ok[i][j - 1]:
                ok[i][j] = True
    return ok[-1][-1]


if __name__ == "__main__":
    print(largest_square(["10100", "10111", "11111", "10010"]), longest_common_substring("ABABC", "BABCA"),
          falling_path_min([[2, 1, 3], [6, 5, 4], [7, 8, 9]]), is_interleaving("aabcc", "dbbca", "aadbbcbcac"))
