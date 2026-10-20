import unittest

import ch09_examples as ex


class TestChapter9(unittest.TestCase):
    def test_cases(self) -> None:
        self.assertEqual([ex.looks(ex.SHELF, b) for b in ex.SHELF], list(range(1, 10)))
        self.assertEqual(ex.looks(ex.SHELF, 50), 9)
        for n in range(1, 200):
            self.assertAlmostEqual(ex.average_looks([1 / n] * n), (n + 1) / 2)
        self.assertAlmostEqual(ex.average_looks(ex.popularity_first(9)), 3.18, places=2)
        self.assertAlmostEqual(ex.average_looks([0.5] + [0.5 / 8] * 8), 3.25)


if __name__ == "__main__":
    unittest.main()
