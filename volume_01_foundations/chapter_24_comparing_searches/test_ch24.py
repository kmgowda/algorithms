import random
import unittest

import ch24_examples as ex


class TestChapter06(unittest.TestCase):
    def test_looks_are_sensible(self) -> None:
        rng = random.Random(1)
        a = sorted(rng.sample(range(100_000), 10_000))
        for k in rng.sample(a, 200):
            self.assertEqual(ex.linear_looks(a, k), a.index(k) + 1)
            self.assertLessEqual(ex.binary_looks(a, k), 16)
            self.assertLessEqual(ex.exponential_looks(a, k), 32)
            self.assertGreaterEqual(ex.interpolation_looks(a, k), 1)

    def test_every_case(self) -> None:
        a = list(range(0, 10_000_000, 10))
        rows = [(0, 1, 21, 4, 1), (9_999_990, 1_000_000, 21, 41, 1), (5_000_000, 500_001, 20, 39, 1),
                (5_000_005, 1_000_000, 21, 39, 1), (-5, 1_000_000, 21, 4, 1)]
        for key, lin, b, e, i in rows:
            self.assertEqual((ex.linear_looks(a, key), ex.binary_looks(a, key), ex.exponential_looks(a, key),
                              ex.interpolation_looks(a, key)), (lin, b, e, i))

    def test_experiment_order(self) -> None:
        out = ex.experiment(n=20_000, queries=200)
        self.assertGreater(out["linear"][0], out["binary"][0])
        self.assertGreater(out["binary"][0], out["interpolation"][0])
        self.assertGreater(out["exponential"][0], out["binary"][0])


if __name__ == "__main__":
    unittest.main()
