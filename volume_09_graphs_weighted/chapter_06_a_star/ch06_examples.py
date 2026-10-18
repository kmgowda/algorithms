"""Volume 9, Chapter 6 - A* Search: Heuristics for Games and Maps.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import heapq
import itertools
import math
from typing import Callable, Hashable, Iterable

Neighbours = Callable[[Hashable], Iterable[tuple[Hashable, float]]]


def a_star(start: Hashable, goal: Hashable, neighbours: Neighbours, h: Callable[[Hashable], float]
           ) -> tuple[float, list[Hashable], int]:
    """Dijkstra, but the heap is ordered by f = g + h: cost so far + estimated cost still to go.
    If h never overestimates (admissible) the answer is optimal. Returns (cost, path, vertices expanded)."""
    g: dict[Hashable, float] = {start: 0.0}
    parent: dict[Hashable, Hashable | None] = {start: None}
    closed: set[Hashable] = set()
    tie = itertools.count()
    heap = [(h(start), next(tie), start)]
    expanded = 0
    while heap:
        _, _, u = heapq.heappop(heap)
        if u in closed:
            continue
        if u == goal:
            path = []
            v: Hashable | None = u
            while v is not None:
                path.append(v)
                v = parent[v]
            return g[u], path[::-1], expanded
        closed.add(u)
        expanded += 1
        for v, w in neighbours(u):
            ng = g[u] + w
            if ng < g.get(v, math.inf):
                g[v], parent[v] = ng, u
                heapq.heappush(heap, (ng + h(v), next(tie), v))
    return math.inf, [], expanded


def grid_neighbours(grid: list[str]) -> Neighbours:
    """4-way moves on a grid; '#' walls; digits are terrain costs (mud = 5); '.' costs 1."""
    rows, cols = len(grid), len(grid[0])

    def nb(cell: Hashable) -> Iterable[tuple[Hashable, float]]:
        r, c = cell                                             # type: ignore[misc]
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                ch = grid[nr][nc]
                yield (nr, nc), float(ch) if ch.isdigit() else 1.0
    return nb


def manhattan(goal: tuple[int, int]) -> Callable[[Hashable], float]:
    """Admissible on 4-way grids where every step costs at least 1: you need at least |dr| + |dc| moves."""
    return lambda cell: abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])      # type: ignore[index]


def zero(_: Hashable) -> float:
    """h = 0 turns A* back into Dijkstra."""
    return 0.0


def game_path(grid: list[str], start: tuple[int, int], goal: tuple[int, int]) -> tuple[float, int, int]:
    """Industry example: a game character crossing a map. Returns (cost, nodes expanded by A*, by Dijkstra)."""
    nb = grid_neighbours(grid)
    cost, _, a_work = a_star(start, goal, nb, manhattan(goal))
    cost2, _, d_work = a_star(start, goal, nb, zero)
    assert cost == cost2
    return cost, a_work, d_work


def open_field_savings(n: int) -> tuple[int, int]:
    """On an open n x n field, corner to corner: vertices expanded by A* vs. Dijkstra."""
    grid = ["." * n] * n
    nb = grid_neighbours(grid)
    goal = (n - 1, n - 1)
    return a_star((0, 0), goal, nb, manhattan(goal))[2], a_star((0, 0), goal, nb, zero)[2]


def straight_line_km(coords: dict[str, tuple[float, float]], goal: str) -> Callable[[Hashable], float]:
    """Industry example: on road maps, the straight-line distance never exceeds the road distance - admissible."""
    gx, gy = coords[goal]
    return lambda city: math.dist(coords[city], (gx, gy))                   # type: ignore[index]


if __name__ == "__main__":
    world = ["..........",
             ".#.#..#.#.",
             ".#......#.",
             ".#.#..#.#.",
             "...#55#...",
             "####..####",
             "..........",
             ]
    print("game path (cost, A* expanded, Dijkstra expanded):", game_path(world, (0, 0), (6, 9)))
    print("open 30x30 field (A*, Dijkstra expanded):", open_field_savings(30))
    coords = {"A": (0, 0), "B": (3, 4), "C": (6, 0), "D": (9, 4)}
    roads = {"A": {"B": 5, "C": 6}, "B": {"D": 6, "C": 5}, "C": {"D": 5.5}, "D": {}}
    print(a_star("A", "D", lambda u: roads[u].items(), straight_line_km(coords, "D")))
