import itertools
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestRecipe(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            offers = [rng.randint(0, 50) for _ in range(rng.randint(0, 12))]
            self.assertEqual(ex.best_tutoring_income(offers), ex.brute_tutoring(offers))
            days = sorted(rng.sample(range(1, 60), rng.randint(1, 9)))
            self.assertEqual(ex.cheapest_tickets(days), ex.brute_tickets(days))
            r, c = rng.randint(1, 5), rng.randint(1, 5)
            grid = [[rng.randint(0, 9) for _ in range(c)] for _ in range(r)]
            moves = [0] * (r - 1) + [1] * (c - 1)
            best = min(sum(grid[y][x] for y, x in self._walk(order)) for order in set(itertools.permutations(moves)))
            self.assertEqual(ex.min_path_cost(grid), best)
            houses = [[rng.randint(1, 20) for _ in range(3)] for _ in range(rng.randint(1, 6))]
            brute = min(sum(houses[i][col] for i, col in enumerate(cs)) for cs in itertools.product(range(3), repeat=len(houses))
                        if all(a != b for a, b in zip(cs, cs[1:])))
            self.assertEqual(sol.paint_houses(houses), brute)

    @staticmethod
    def _walk(order):
        y = x = 0
        yield 0, 0
        for m in order:
            if m == 0:
                y += 1
            else:
                x += 1
            yield y, x

    def test_examples(self) -> None:
        self.assertEqual(ex.best_tutoring_income([30, 10, 50, 40, 20, 60]), 140)
        self.assertEqual(ex.cheapest_tickets([1, 4, 6, 7, 8, 20]), 11)
        self.assertEqual(ex.cheapest_tickets(list(range(1, 31))), 15)
        self.assertEqual(ex.min_path_cost([[1, 3, 1], [1, 5, 1], [4, 2, 1]]), 7)
        self.assertEqual(sol.max_points_deleting([2, 2, 3, 3, 3, 4]), 9)
        self.assertEqual(sol.paint_houses([[17, 2, 17], [16, 16, 5], [14, 3, 19]]), 10)
        self.assertIn("state", sol.describe_recipe("tutor"))


if __name__ == "__main__":
    unittest.main()
