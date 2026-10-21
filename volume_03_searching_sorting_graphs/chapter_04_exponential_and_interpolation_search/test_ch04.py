import bisect
import random
import unittest

import ch04_examples as ex


class TestChapter04(unittest.TestCase):
    def test_exponential(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            values = sorted(rng.sample(range(1000), rng.randint(1, 60)))
            for key in range(-1, 1001, 7):
                got = ex.exponential_search(ex.Reel(values), key)
                self.assertEqual(got, values.index(key) if key in values else -1)
        t = []
        reel = ex.Reel(range(3, 3000, 3))
        self.assertEqual(ex.exponential_search(reel, 87, t), 28)
        self.assertEqual([x[1] for x in t if x[0] == "gallop"], [1, 2, 4, 8, 16, 32])
        self.assertEqual([x[1] for x in t if x[0] == "binary"], [24, 28, 26, 27])
        self.assertEqual(reel.reads, 11)

    def test_interpolation(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            values = sorted(set(rng.randint(0, 500) for _ in range(rng.randint(1, 40))))
            for key in range(-1, 502, 3):
                i = ex.interpolation_search(values, key)
                self.assertEqual(i, bisect.bisect_left(values, key) if key in values else -1)
        t = []
        self.assertEqual(ex.interpolation_search([12, 25, 31, 47, 58, 63, 70, 84, 91], 70, t), 6)
        self.assertEqual(t, [(0, 8, 5, 63), (6, 8, 6, 70)])

    def test_uniform_beats_binary(self) -> None:
        rng = random.Random(1)
        a = sorted(rng.sample(range(1_000_000), 50_000))
        b, i = ex.average_looks(a, rng.sample(a, 300))
        self.assertLess(i, b)


if __name__ == "__main__":
    unittest.main()
