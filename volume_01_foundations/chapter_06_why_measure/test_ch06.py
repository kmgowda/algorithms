import math
import unittest

import ch06_examples as ex


class TestChapter6(unittest.TestCase):
    def test_every_case(self) -> None:
        shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
        self.assertEqual([ex.search_comparisons(shelf, t) for t in (12, 58, 91, 50)], [1, 5, 9, 9])
        self.assertEqual(ex.search_comparisons([], 5), 0)
        self.assertEqual([ex.pair_comparisons(n) for n in (0, 1, 2, 3, 10)], [0, 0, 1, 3, 45])
        sizes = [1000, 2000, 4000, 8000]
        self.assertEqual(ex.doubling_ratios([5] * 4), [1.0] * 3)
        self.assertEqual(ex.doubling_ratios(sizes), [2.0] * 3)
        self.assertEqual(ex.doubling_ratios([n * (n - 1) // 2 for n in sizes]), [4.0] * 3)
        self.assertEqual(ex.doubling_ratios([n ** 3 for n in sizes]), [8.0] * 3)

    def test_counts(self) -> None:
        shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
        self.assertEqual(ex.search_comparisons(shelf, 63), 6)
        self.assertEqual(ex.search_comparisons(shelf, 50), 9)
        for n in range(0, 60):
            self.assertEqual(ex.pair_comparisons(n), n * (n - 1) // 2)
        self.assertEqual(ex.pair_comparisons(10), 45)
        self.assertEqual(ex.doubling_ratios([300, 1200, 4800, 19200]), [4.0, 4.0, 4.0])
        self.assertEqual(ex.doubling_ratios([1000, 2000, 4000]), [2.0, 2.0])
        self.assertEqual(len(ex.repeated_timings(1000, 3)), 3)


    def test_doubling_exponents(self) -> None:
        sizes = [1000, 2000, 4000, 8000]
        self.assertEqual(ex.doubling_exponents([n * (n - 1) // 2 for n in sizes]), [2.0, 2.0, 2.0])
        self.assertEqual(ex.doubling_exponents(sizes), [1.0, 1.0, 1.0])
        self.assertEqual(ex.doubling_exponents([0.21, 0.59, 1.68]), [1.49, 1.51])
        self.assertAlmostEqual(ex.predict_after_doubling(1.68, 1.5), 4.75, places=2)
        self.assertEqual(ex.doubling_exponents([1, 8, 64]), [3.0, 3.0])
        self.assertEqual(ex.doubling_exponents([5.0]), [])
        nlogn = [n * math.log2(n) for n in sizes]
        self.assertEqual(ex.doubling_exponents(nlogn), [1.14, 1.13, 1.12])

if __name__ == "__main__":
    unittest.main()
