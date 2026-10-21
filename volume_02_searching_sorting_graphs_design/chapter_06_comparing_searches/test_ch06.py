import random
import unittest

import ch06_examples as ex


class TestChapter06(unittest.TestCase):
    def test_looks_are_sensible(self) -> None:
        rng = random.Random(1)
        a = sorted(rng.sample(range(100_000), 10_000))
        for k in rng.sample(a, 200):
            self.assertEqual(ex.linear_looks(a, k), a.index(k) + 1)
            self.assertLessEqual(ex.binary_looks(a, k), 16)
            self.assertLessEqual(ex.exponential_looks(a, k), 32)
            self.assertGreaterEqual(ex.interpolation_looks(a, k), 1)

    def test_experiment_order(self) -> None:
        out = ex.experiment(n=20_000, queries=200)
        self.assertGreater(out["linear"][0], out["binary"][0])
        self.assertGreater(out["binary"][0], out["interpolation"][0])
        self.assertGreater(out["exponential"][0], out["binary"][0])


if __name__ == "__main__":
    unittest.main()
