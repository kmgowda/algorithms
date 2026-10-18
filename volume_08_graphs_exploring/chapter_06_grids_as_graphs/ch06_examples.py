"""Volume 8, Chapter 6 - Grids as Graphs: Islands, Flood Fill, Rotting Oranges.

Every cell (r, c) is a vertex; its up/down/left/right neighbours are its edges. No graph is ever built.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Iterator

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbours(grid: list[list[str]], r: int, c: int) -> Iterator[tuple[int, int]]:
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


def count_islands(grid: list[list[str]]) -> int:
    """LeetCode 200: '#' is land. Each new unvisited land cell starts an island; sink the whole island with DFS."""
    seen: set[tuple[int, int]] = set()
    islands = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "#" and (r, c) not in seen:
                islands += 1
                stack = [(r, c)]
                seen.add((r, c))
                while stack:
                    cell = stack.pop()
                    for nr, nc in neighbours(grid, *cell):
                        if grid[nr][nc] == "#" and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            stack.append((nr, nc))
    return islands


def flood_fill(image: list[list[str]], r: int, c: int, new: str) -> list[list[str]]:
    """LeetCode 733 - the paint bucket tool: recolour the connected region of the same colour."""
    out = [row[:] for row in image]
    old = out[r][c]
    if old == new:
        return out
    stack = [(r, c)]
    out[r][c] = new
    while stack:
        cell = stack.pop()
        for nr, nc in neighbours(out, *cell):
            if out[nr][nc] == old:
                out[nr][nc] = new
                stack.append((nr, nc))
    return out


def rotting_minutes(grid: list[list[str]]) -> int:
    """LeetCode 994: 'R' rotten, 'F' fresh, '.' empty. Each minute rot spreads to neighbours.
    Multi-source BFS from all rotten oranges; answer = last ring reached, or -1 if some fruit never rots."""
    queue = deque((r, c, 0) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == "R")
    fresh = sum(row.count("F") for row in grid)
    seen = {(r, c) for r, c, _ in queue}
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        minutes = max(minutes, t)
        for nr, nc in neighbours(grid, r, c):
            if grid[nr][nc] == "F" and (nr, nc) not in seen:
                seen.add((nr, nc))
                fresh -= 1
                queue.append((nr, nc, t + 1))
    return minutes if fresh == 0 else -1


def shortest_walk(grid: list[list[str]], start: tuple[int, int], goal: tuple[int, int]) -> int:
    """Practical example: fewest steps through a maze ('#' walls) - BFS on cells."""
    if grid[start[0]][start[1]] == "#":
        return -1
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == goal:
            return dist[cell]
        for nxt in neighbours(grid, *cell):
            if grid[nxt[0]][nxt[1]] != "#" and nxt not in dist:
                dist[nxt] = dist[cell] + 1
                queue.append(nxt)
    return -1


def to_grid(rows: list[str]) -> list[list[str]]:
    return [list(r) for r in rows]


if __name__ == "__main__":
    sea = to_grid(["##..#", "#...#", "..#..", "....#"])
    print("islands:", count_islands(sea))
    img = to_grid(["aab", "abb", "bbb"])
    print("flood fill:", ["".join(r) for r in flood_fill(img, 0, 0, "z")])
    print("rotting minutes:", rotting_minutes(to_grid(["RF.", "FF.", ".FF"])), rotting_minutes(to_grid(["RF", ".F", "F."])))
    maze = to_grid(["S..#", ".#..", "...#", "#.G."])
    print("maze steps:", shortest_walk(maze, (0, 0), (3, 2)))
