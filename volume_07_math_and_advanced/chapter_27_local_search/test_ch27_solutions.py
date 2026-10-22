import itertools
import random
import unittest

import ch27_examples as ex
import ch27_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_max_cut_moves_bounded(self) -> None:
        r = random.Random(27)
        for _ in range(150):
            vs = list(range(r.randint(1, 8)))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.4]
            side, cut, moves = ex.max_cut_local(vs, es)
            self.assertLessEqual(moves, len(es))
            self.assertGreaterEqual(2 * cut, len(es))

    def test_restarts(self) -> None:
        self.assertEqual((sol.restarts_needed(0.3), sol.restarts_needed(0.5), sol.restarts_needed(1.0)), (13, 7, 1))
        for p in (0.05, 0.3, 0.5, 0.9):
            r = sol.restarts_needed(p)
            self.assertGreaterEqual(1 - (1 - p) ** r, 0.99)
            self.assertLess(1 - (1 - p) ** (r - 1), 0.99)
        with self.assertRaises(ValueError):
            sol.restarts_needed(0)

    def test_acceptance(self) -> None:
        self.assertAlmostEqual(sol.accept_probability(10, 10), 0.36788, places=4)
        self.assertEqual(sol.accept_probability(-3, 10), 1.0)
        for d in (0.1, 1, 10, 100):
            self.assertEqual(sol.buggy_accept_probability(d, 5), 1.0)
            self.assertLess(sol.accept_probability(d, 5), 1.0)


if __name__ == "__main__":
    unittest.main()
