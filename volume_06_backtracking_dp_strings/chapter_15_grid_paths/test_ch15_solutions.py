import math
import random
import unittest

import ch15_examples as ex
import ch15_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_binomial(self) -> None:
        for r in range(1, 9):
            for c in range(1, 9):
                self.assertEqual(ex.count_paths([[0] * c for _ in range(r)])[0], math.comb(r + c - 2, r - 1))

    def test_through(self) -> None:
        self.assertEqual(sol.paths_through(ex.FLOOR, 2, 2), sol.brute_through(ex.FLOOR, 2, 2))
        rnd = random.Random(15)
        for _ in range(150):
            rows, cols = rnd.randint(1, 5), rnd.randint(1, 5)
            floor = [[1 if rnd.random() < 0.2 else 0 for _ in range(cols)] for _ in range(rows)]
            floor[0][0] = 0
            lr, lc = rnd.randrange(rows), rnd.randrange(cols)
            self.assertEqual(sol.paths_through(floor, lr, lc), sol.brute_through(floor, lr, lc))

    def test_empty(self) -> None:
        self.assertEqual(ex.count_paths([]), (0, []))
        with self.assertRaises(ValueError):
            ex.cheapest([])


if __name__ == "__main__":
    unittest.main()
