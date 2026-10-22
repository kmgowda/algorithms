"""Volume 6, Chapter 15 - Paths Through a Grid: count routes and find the cheapest, moving only right or down.

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

import math

# The archive floor: 0 = open, 1 = a shelf in the way. Start top-left, finish bottom-right.
FLOOR = [[0, 0, 0, 0, 0],
         [0, 1, 0, 1, 0],
         [0, 0, 0, 0, 0],
         [1, 0, 1, 0, 0]]
# Dust on each square of the reading room (minutes of sneezing!), for the cheapest route.
DUST = [[1, 3, 1, 2],
        [1, 5, 1, 9],
        [4, 2, 1, 3],
        [7, 1, 8, 1]]


def count_paths(floor: list) -> tuple[int, list]:
    """paths[r][c] = paths[r-1][c] + paths[r][c-1] on open squares (Figure 15.2)."""
    rows, cols = len(floor), len(floor[0])
    paths = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if floor[r][c]:
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                paths[r][c] = (paths[r - 1][c] if r else 0) + (paths[r][c - 1] if c else 0)
    return paths[-1][-1], paths


def cheapest(dust: list) -> tuple[int, list, list]:
    """least[r][c] = dust[r][c] + min(above, left) (Figure 15.3). Returns (total, table, route)."""
    rows, cols = len(dust), len(dust[0])
    least = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            options = ([least[r - 1][c]] if r else []) + ([least[r][c - 1]] if c else [])
            least[r][c] = dust[r][c] + (min(options) if options else 0)
    route, r, c = [(rows - 1, cols - 1)], rows - 1, cols - 1
    while (r, c) != (0, 0):
        if c == 0 or (r > 0 and least[r - 1][c] <= least[r][c - 1]):
            r -= 1
        else:
            c -= 1
        route.append((r, c))
    return least[-1][-1], least, route[::-1]


def count_paths_moving(floor: list, k: int) -> tuple[int, list]:
    """Routes that may pass through at most k shelf squares (the trolley can push a shelf aside, but only k times)
    (Section 15.6). State (r, c, j): routes reaching (r, c) having pushed exactly j shelves.
    Returns (routes with at most k pushes, the counts at the far corner for j = 0..k)."""
    rows, cols = len(floor), len(floor[0])
    ways = [[[0] * (k + 1) for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            for j in range(k + 1):
                shelf = floor[r][c]
                before = j - shelf                     # pushes used before arriving here
                if before < 0:
                    continue
                if r == 0 and c == 0:
                    ways[r][c][j] = 1 if before == 0 else 0
                else:
                    ways[r][c][j] = (ways[r - 1][c][before] if r else 0) + (ways[r][c - 1][before] if c else 0)
    corner = ways[-1][-1]
    return sum(corner), corner


if __name__ == "__main__":
    n, table = count_paths(FLOOR)
    print(n, table)
    print(count_paths([[0] * 5 for _ in range(4)])[0], math.comb(7, 3))
    print(cheapest(DUST))
