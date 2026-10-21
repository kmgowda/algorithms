"""Volume 2, Chapter 9 - Grid Techniques: Flood Fill and Counting Regions.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

from collections import deque

ROOM = ["11000", "11011", "00010", "10000", "10111"]
FLOOR = ["##########",
         "#E.....#.#",
         "#.##.#.#.#",
         "#....#...#",
         "####.###.#",
         "#....#...#",
         "#.####.###",
         "#......#.#",
         "##########"]


def study_groups(grid: list[str]) -> list[int]:
    """Sizes of the groups of side-by-side occupied seats ('1'), found by flood fill (Figure 9.1)."""
    rows, cols, visited, sizes = len(grid), len(grid[0]), set(), []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                stack, size = [(r, c)], 0
                visited.add((r, c))
                while stack:
                    a, b = stack.pop()
                    size += 1
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < rows and 0 <= y < cols and grid[x][y] == "1" and (x, y) not in visited:
                            visited.add((x, y))
                            stack.append((x, y))
                sizes.append(size)
    return sizes


def groups_with_diagonals(grid: list[str]) -> int:
    """Exercise 1: count groups when the 8 surrounding cells all count as touching."""
    rows, cols, seen, count = len(grid), len(grid[0]), set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                count += 1
                stack = [(r, c)]
                seen.add((r, c))
                while stack:
                    a, b = stack.pop()
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            x, y = a + dx, b + dy
                            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == "1" and (x, y) not in seen:
                                seen.add((x, y))
                                stack.append((x, y))
    return count


def distances_from_exit(floor: list[str]) -> dict[tuple[int, int], int]:
    """Section 9.7: breadth-first flood fill from 'E' through open squares; steps to every reachable square."""
    start = next((r, c) for r, row in enumerate(floor) for c, ch in enumerate(row) if ch == "E")
    dist = {start: 0}
    q = deque([start])
    while q:
        a, b = q.popleft()
        for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
            if floor[x][y] != "#" and (x, y) not in dist:
                dist[(x, y)] = dist[(a, b)] + 1
                q.append((x, y))
    return dist


def cut_off(floor: list[str]) -> list[tuple[int, int]]:
    """Open squares that cannot reach the exit."""
    reach = distances_from_exit(floor)
    return [(r, c) for r, row in enumerate(floor) for c, ch in enumerate(row) if ch == "." and (r, c) not in reach]


if __name__ == "__main__":
    print(study_groups(ROOM), groups_with_diagonals(ROOM), study_groups(["101", "010", "101"]))
    d = distances_from_exit(FLOOR)
    print(max(d.values()), cut_off(FLOOR))
