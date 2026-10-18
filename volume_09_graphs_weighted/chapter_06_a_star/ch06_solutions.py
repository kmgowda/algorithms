"""Volume 9, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch06_examples import a_star, grid_neighbours, manhattan


def sliding_puzzle(board: tuple[int, ...]) -> int:
    """Exercise 1 (LeetCode 773): 2x3 sliding puzzle (0 = blank) to (1,2,3,4,5,0) in fewest moves.
    Heuristic: sum of Manhattan distances of tiles from their homes (admissible: each move shifts one tile by 1)."""
    goal = (1, 2, 3, 4, 5, 0)
    moves = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}

    def neighbours(state: Hashable):
        s = list(state)                                          # type: ignore[arg-type]
        z = s.index(0)
        for m in moves[z]:
            t = s[:]
            t[z], t[m] = t[m], t[z]
            yield tuple(t), 1.0

    def h(state: Hashable) -> float:
        total = 0
        for i, tile in enumerate(state):                          # type: ignore[arg-type]
            if tile:
                home = tile - 1
                total += abs(i // 3 - home // 3) + abs(i % 3 - home % 3)
        return total

    cost, path, _ = a_star(board, goal, neighbours, h)
    return int(cost) if path else -1


def overestimating_heuristic_breaks() -> tuple[float, float]:
    """Exercise 2: a heuristic that overestimates (here 10 x Manhattan) finds A path fast - but maybe not the best."""
    grid = ["....", ".55.", "....", "...."]
    nb = grid_neighbours(grid)
    good = a_star((0, 0), (3, 3), nb, manhattan((3, 3)))[0]
    greedy = a_star((0, 0), (3, 3), nb, lambda c: 10 * manhattan((3, 3))(c))[0]
    return good, greedy


def weighted_terrain_cost(grid: list[str], start: tuple[int, int], goal: tuple[int, int]) -> float:
    """Exercise 3: the cheapest route cost on a terrain map."""
    return a_star(start, goal, grid_neighbours(grid), manhattan(goal))[0]


if __name__ == "__main__":
    print(sliding_puzzle((4, 1, 2, 5, 0, 3)), sliding_puzzle((1, 2, 3, 5, 4, 0)))
    print(overestimating_heuristic_breaks(), weighted_terrain_cost([".9.", "...", "..."], (0, 0), (0, 2)))
