import random
import unittest

import ch01_examples as ex


class TestChapter1(unittest.TestCase):
    def test_tallest(self) -> None:
        rng = random.Random(1)
        self.assertEqual(ex.tallest(ex.HEIGHTS), 161)
        self.assertEqual(ex.tallest([150, 150, 149]), 150)
        for _ in range(200):
            xs = [rng.randint(100, 200) for _ in range(rng.randint(1, 20))]
            self.assertEqual(ex.tallest(xs), max(xs))

    def test_two_ways(self) -> None:
        self.assertEqual((ex.looks_one_by_one(ex.SHELF, 63), ex.looks_by_halving(ex.SHELF, 63)), (6, 3))
        self.assertEqual((ex.looks_one_by_one(ex.SHELF, 91), ex.looks_by_halving(ex.SHELF, 91)), (9, 4))
        big = list(range(1_000_000))
        self.assertLessEqual(max(ex.looks_by_halving(big, t) for t in (0, 999_999, 500_000, 123_457)), 20)


if __name__ == "__main__":
    unittest.main()
