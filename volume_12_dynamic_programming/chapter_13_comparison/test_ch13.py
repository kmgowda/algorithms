import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestComparison(unittest.TestCase):
    def test_methods(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            jobs = []
            for _ in range(rng.randint(0, 9)):
                s = rng.randint(0, 15)
                jobs.append((s, s + rng.randint(1, 6), rng.randint(1, 50)))
            best = ex.backtracking(jobs)
            self.assertEqual(ex.dynamic_programming(jobs), best)
            self.assertLessEqual(ex.greedy_earliest_end(jobs), best)
            self.assertLessEqual(ex.greedy_best_pay(jobs), best)

    def test_examples(self) -> None:
        jobs = [(1, 6, 40), (2, 3, 10), (4, 9, 80), (7, 10, 60)]
        self.assertEqual((ex.greedy_earliest_end(jobs), ex.greedy_best_pay(jobs), ex.dynamic_programming(jobs)), (90, 90, 100))
        r = ex.race(22)
        self.assertLess(r["dynamic programming"], r["backtracking"])
        self.assertEqual(sol.classify()["solve a Sudoku"], "backtracking")
        self.assertIn("bitmask", sol.state_size("TSP"))
        self.assertEqual(ex.choose_paradigm(set()), "brute-force baseline, then look for structure")


if __name__ == "__main__":
    unittest.main()
