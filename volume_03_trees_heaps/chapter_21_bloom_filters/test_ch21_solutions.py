import math
import unittest

import ch21_examples as ex
import ch21_solutions as sol


class TestChapter21Solutions(unittest.TestCase):
    def test_fold_equals_smaller_filter(self) -> None:
        for m in (2, 16, 1000):
            big, small = ex.BloomFilter(m, 3), ex.BloomFilter(m // 2, 3)
            for t in ("Maps", "Ocean", "Clocks", "Stars"):
                big.add(t)
                small.add(t)
            self.assertEqual(sol.fold(big).bits, small.bits)
        empty = sol.fold(ex.BloomFilter(16, 3))
        self.assertEqual(sum(empty.bits), 0)

    def test_estimate_smallest(self) -> None:
        f = sol.CountingOnesFilter(64, 3)
        self.assertEqual(f.estimate(), 0)
        f.add("Maps")
        f.add("Maps")                                        # a repeat adds no bits
        self.assertEqual(f.ones, 3)
        self.assertAlmostEqual(f.estimate(), -64 / 3 * math.log(1 - 3 / 64))
        tiny = sol.CountingOnesFilter(1, 1)
        tiny.add("x")
        self.assertEqual(tiny.estimate(), math.inf)

    def test_estimate_accuracy(self) -> None:
        for n in (10, 100, 1000):
            f = sol.CountingOnesFilter(10 * n, 7)
            for i in range(n):
                f.add(f"book-{i}")
            self.assertEqual(f.ones, sum(f.bits))
            self.assertLess(abs(f.estimate() - n) / n, 0.1)

    def test_neighbour_bits_bug(self) -> None:
        good, bad = sol.compare_rates(trials=20_000)
        self.assertLess(good, 0.012)
        self.assertGreater(bad, 0.15)


if __name__ == "__main__":
    unittest.main()
