"""Volume 8, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque

from ch06_examples import neighbours, to_grid


def largest_island(grid: list[list[str]]) -> int:
    """Exercise 1 (LeetCode 695): the area of the biggest island."""
    seen, best = set(), 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "#" and (r, c) not in seen:
                seen.add((r, c))
                stack, area = [(r, c)], 0
                while stack:
                    cell = stack.pop()
                    area += 1
                    for nr, nc in neighbours(grid, *cell):
                        if grid[nr][nc] == "#" and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            stack.append((nr, nc))
                best = max(best, area)
    return best


def distance_to_nearest_exit(grid: list[list[str]]) -> list[list[int]]:
    """Exercise 2 (LeetCode 542 idea): for every open cell, steps to the nearest 'E' exit (multi-source BFS). -1 if none."""
    dist = [[-1] * len(grid[0]) for _ in grid]
    queue = deque()
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "E":
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in neighbours(grid, r, c):
            if grid[nr][nc] != "#" and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


def surrounded_regions(board: list[list[str]]) -> list[list[str]]:
    """Exercise 3 (LeetCode 130): capture 'O' regions not connected to the border; start from the border's O's."""
    out = [row[:] for row in board]
    rows, cols = len(out), len(out[0])
    stack = [(r, c) for r in range(rows) for c in range(cols)
             if out[r][c] == "O" and (r in (0, rows - 1) or c in (0, cols - 1))]
    safe = set(stack)
    while stack:
        cell = stack.pop()
        for nr, nc in neighbours(out, *cell):
            if out[nr][nc] == "O" and (nr, nc) not in safe:
                safe.add((nr, nc))
                stack.append((nr, nc))
    for r in range(rows):
        for c in range(cols):
            if out[r][c] == "O" and (r, c) not in safe:
                out[r][c] = "X"
    return out


if __name__ == "__main__":
    print(largest_island(to_grid(["##..#", "#...#", "..#..", "....#"])))
    print(distance_to_nearest_exit(to_grid(["E..", ".#.", "..E"])))
    print(["".join(r) for r in surrounded_regions(to_grid(["XXXX", "XOOX", "XXOX", "XOXX"]))])
