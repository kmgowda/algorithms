import random
import unittest

import ch23_examples as ex
import ch23_solutions as sol


def brute_pushes(grid, start, goal):
    """Try every set of shelves, smallest first (tiny grids only)."""
    from itertools import combinations
    shelves = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "#"]
    for k in range(len(shelves) + 1):
        for gone in combinations(shelves, k):
            g = ["".join("." if (r, c) in gone else ch for c, ch in enumerate(row)) for r, row in enumerate(grid)]
            if g[start[0]][start[1]] != "#" and ex.bfs_grid(g, start, goal)[0] is not None:
                return k
    return None


class TestChapter20Solutions(unittest.TestCase):
    def test_fewest_pushes(self) -> None:
        self.assertEqual(sol.fewest_pushes(ex.BASEMENT, (0, 0), (4, 7)), 0)
        self.assertEqual(sol.fewest_pushes(["S.#.", "..#E", "..#."], (0, 0), (1, 3)), 1)
        self.assertEqual(sol.fewest_pushes(["S.#.#E", "..#.#.", "..#.#."], (0, 0), (0, 5)), 2)
        self.assertEqual(sol.fewest_pushes(["S#.#E"], (0, 0), (0, 4)), 2)

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.fewest_pushes(["S"], (0, 0), (0, 0)), 0)
        self.assertEqual(sol.fewest_pushes(["S#"], (0, 0), (0, 1)), 1)          # the goal itself is a shelf
        self.assertIsNone(sol.fewest_pushes(["S"], (0, 0), (0, 1)))            # goal outside the grid
        self.assertIsNone(sol.fewest_pushes([], (0, 0), (0, 0)))

    def test_against_brute_force(self) -> None:
        rng = random.Random(20)
        for _ in range(200):
            rows, cols = rng.randint(1, 3), rng.randint(1, 4)
            grid = ["".join("#" if rng.random() < 0.45 else "." for _ in range(cols)) for _ in range(rows)]
            grid[0] = "." + grid[0][1:]
            goal = (rows - 1, cols - 1)
            self.assertEqual(sol.fewest_pushes(grid, (0, 0), goal), brute_pushes(grid, (0, 0), goal), grid)

    def test_parity(self) -> None:
        lengths = set()
        for i, row in enumerate(ex.BASEMENT):
            for j, ch in enumerate(row):
                if ch == "#":
                    g = ["".join("." if (r, c) == (i, j) else x for c, x in enumerate(rw))
                         for r, rw in enumerate(ex.BASEMENT)]
                    lengths.add(len(ex.bfs_grid(g, (0, 0), (4, 7))[0]) - 1)
        self.assertEqual(lengths, {11, 13, 15})

    def test_corner_rule(self) -> None:
        self.assertEqual(sol.corner_rule_rooms([".#.", "..."]), 2)
        self.assertEqual(sol.rooms([".#.", "..."]), 1)
        self.assertEqual(sol.corner_rule_rooms(ex.BASEMENT), 4)
        self.assertEqual(sol.rooms(ex.BASEMENT), 1)
        self.assertEqual(sol.rooms(["..#..", "..#..", "#####", "....."]), 3)
        self.assertEqual(sol.corner_rule_rooms(["..#..", "..#..", "#####", "....."]), 3)
        self.assertEqual(sol.rooms([]), 0)
        self.assertEqual(sol.rooms(["#"]), 0)


if __name__ == "__main__":
    unittest.main()
