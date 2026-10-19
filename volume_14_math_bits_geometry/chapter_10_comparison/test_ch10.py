import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestMathVsSimulation(unittest.TestCase):
    def test_agree(self) -> None:
        rng = random.Random(1)
        for n in range(0, 300):
            self.assertEqual(ex.sum_formula(n), ex.sum_simulated(n))
            self.assertEqual(sol.sum_of_squares(n), sum(i * i for i in range(n + 1)))
        for _ in range(100):
            n, k = rng.randint(1, 60), rng.randint(1, 10)
            self.assertEqual(ex.josephus_formula(n, k), ex.josephus_simulated(n, k))
        for n in range(1, 200):
            self.assertEqual(sol.josephus_every_second(n), ex.josephus_simulated(n, 2))
        for r in range(1, 7):
            for c in range(1, 7):
                self.assertEqual(ex.grid_paths_formula(r, c), ex.grid_paths_enumerated(r, c))
        self.assertAlmostEqual(ex.birthday_simulated(23, 20000, rng), ex.birthday_formula(23), delta=0.02)

    def test_race_and_guide(self) -> None:
        r = ex.race()
        for name, (sim, formula) in r.items():
            self.assertLess(formula, sim, name)
        self.assertEqual(sol.josephus_every_second(41), 19)
        self.assertEqual(sol.pick_approaches()["total of 1..n"], "formula")
        self.assertEqual(ex.choose_approach(set()), "simulate small cases, then look for a pattern and prove it")


if __name__ == "__main__":
    unittest.main()
