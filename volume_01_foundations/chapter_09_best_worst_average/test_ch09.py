import unittest

import ch09_examples as ex


class TestChapter9(unittest.TestCase):
    def test_every_case(self) -> None:
        pf = ex.popularity_first(9)
        self.assertEqual(ex.average_looks([1] + [0] * 8), 1)
        self.assertEqual(round(ex.average_looks(pf), 2), 3.18)
        self.assertAlmostEqual(ex.average_looks([1 / 9] * 9), 5)
        self.assertEqual(round(ex.average_looks(pf[::-1]), 2), 6.82)
        self.assertAlmostEqual(0.5 * 9 + 0.5 * ex.average_looks([1 / 9] * 9), 7)
        self.assertEqual(ex.average_looks([0] * 8 + [1]), 9)
        self.assertEqual((ex.looks([47], 47), ex.looks([47], 12), ex.looks([], 5)), (1, 1, 0))

    def test_cases(self) -> None:
        self.assertEqual([ex.looks(ex.SHELF, b) for b in ex.SHELF], list(range(1, 10)))
        self.assertEqual(ex.looks(ex.SHELF, 50), 9)
        for n in range(1, 200):
            self.assertAlmostEqual(ex.average_looks([1 / n] * n), (n + 1) / 2)
        self.assertAlmostEqual(ex.average_looks(ex.popularity_first(9)), 3.18, places=2)
        self.assertAlmostEqual(ex.average_looks([0.5] + [0.5 / 8] * 8), 3.25)

    def test_misses_formula(self) -> None:
        self.assertEqual(ex.average_with_misses(9, 0.5), 7)
        self.assertEqual(ex.average_with_misses(9, 1), 5)
        self.assertEqual(ex.average_with_misses(9, 0), 9)
        self.assertEqual(ex.average_with_misses(0, 0.5), 0)
        self.assertEqual(ex.average_with_misses(1, 0.3), 1)
        self.assertAlmostEqual(ex.average_with_misses(100, 0.75), 62.875)
        for n in range(1, 30):
            shares = [0.5 / n] * n
            self.assertAlmostEqual(ex.average_with_misses(n, 0.5), ex.average_looks(shares) + 0.5 * n)

    def test_harmonic(self) -> None:
        self.assertEqual(ex.harmonic(0), 0)
        self.assertEqual(ex.harmonic(1), 1)
        self.assertAlmostEqual(9 / ex.harmonic(9), ex.average_looks(ex.popularity_first(9)))
        self.assertEqual(round(ex.harmonic(9), 2), 2.83)


    def test_indicators(self) -> None:
        self.assertEqual(ex.updates(ex.TALLEST), 2)
        for n in range(1, 8):
            self.assertAlmostEqual(ex.average_updates(n), ex.harmonic(n) - 1)
        self.assertAlmostEqual(ex.harmonic(6) - 1, 1.45, places=2)


if __name__ == "__main__":
    unittest.main()
