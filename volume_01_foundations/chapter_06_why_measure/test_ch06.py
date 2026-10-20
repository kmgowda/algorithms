import unittest

import ch06_examples as ex


class TestChapter6(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
