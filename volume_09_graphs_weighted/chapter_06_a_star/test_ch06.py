import math
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestAStar(unittest.TestCase):
    def test_matches_dijkstra_on_random_grids(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            rows, cols = rng.randint(2, 8), rng.randint(2, 8)
            grid = ["".join(rng.choice("....#59") for _ in range(cols)) for _ in range(rows)]
            grid[0] = "." + grid[0][1:]
            grid[-1] = grid[-1][:-1] + "."
            nb = ex.grid_neighbours(grid)
            goal = (rows - 1, cols - 1)
            a = ex.a_star((0, 0), goal, nb, ex.manhattan(goal))
            d = ex.a_star((0, 0), goal, nb, ex.zero)
            self.assertEqual(a[0], d[0])
            self.assertLessEqual(a[2], d[2])
            if a[1]:
                steps = list(zip(a[1], a[1][1:]))
                cost = sum(float(grid[r][c]) if grid[r][c].isdigit() else 1.0 for _, (r, c) in steps)
                self.assertEqual(cost, a[0])

    def test_examples(self) -> None:
        world = ["..........", ".########.", ".#......#.", ".#.#..#.#.", "...#55#...", "####..####", ".........."]
        cost, a_work, d_work = ex.game_path(world, (0, 0), (6, 9))
        self.assertLess(a_work, d_work)
        a_open, d_open = ex.open_field_savings(20)
        self.assertLess(a_open * 3, d_open)
        coords = {"A": (0, 0), "B": (3, 4), "C": (6, 0), "D": (9, 4)}
        roads = {"A": {"B": 5, "C": 6}, "B": {"D": 6, "C": 5}, "C": {"D": 5.5}, "D": {}}
        self.assertEqual(ex.a_star("A", "D", lambda u: roads[u].items(), ex.straight_line_km(coords, "D"))[:2], (11, ["A", "B", "D"]))
        self.assertEqual(ex.a_star((0, 0), (0, 2), ex.grid_neighbours([".#."]), ex.manhattan((0, 2)))[0], math.inf)

    def test_solutions(self) -> None:
        self.assertEqual(sol.sliding_puzzle((4, 1, 2, 5, 0, 3)), 5)
        self.assertEqual(sol.sliding_puzzle((1, 2, 3, 5, 4, 0)), -1)
        self.assertEqual(sol.sliding_puzzle((1, 2, 3, 4, 5, 0)), 0)
        good, greedy = sol.overestimating_heuristic_breaks()
        self.assertLessEqual(good, greedy)
        self.assertEqual(sol.weighted_terrain_cost([".9.", "...", "..."], (0, 0), (0, 2)), 4)


if __name__ == "__main__":
    unittest.main()
