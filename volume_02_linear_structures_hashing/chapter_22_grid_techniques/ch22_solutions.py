"""Volume 2, Chapter 22 - Thinking Problem solutions (Section 22.15)."""

from __future__ import annotations


def best_extra_seat(grid: list[str]) -> tuple[int, tuple[int, int] | None]:
    """Thinking Problem 22.2: the largest group possible after occupying at most one empty seat.

    Returns (size, seat), seat None if no empty seat helps. Two passes, O(rows x columns)."""
    rows, cols = len(grid), len(grid[0]) if grid else 0
    label: dict[tuple[int, int], int] = {}
    sizes: list[int] = []
    for r in range(rows):                              # pass 1: label every group by flood fill
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in label:
                label[(r, c)] = len(sizes)
                stack, size = [(r, c)], 0
                while stack:
                    a, b = stack.pop()
                    size += 1
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < rows and 0 <= y < cols and grid[x][y] == "1" and (x, y) not in label:
                            label[(x, y)] = len(sizes)
                            stack.append((x, y))
                sizes.append(size)
    best = (max(sizes, default=0), None)
    for r in range(rows):                              # pass 2: try every empty seat
        for c in range(cols):
            if grid[r][c] == "0":
                touching = {label[n] for n in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if n in label}
                total = 1 + sum(sizes[g] for g in touching)
                if total > best[0]:
                    best = (total, (r, c))
    return best


def count_by_corners(grid: list[str]) -> int:
    """Thinking Problem 22.3: the buggy one-pass count (a seat starts a group if nothing sits above or left)."""
    count = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "1" and not (r and grid[r - 1][c] == "1") and not (c and row[c - 1] == "1"):
                count += 1
    return count
