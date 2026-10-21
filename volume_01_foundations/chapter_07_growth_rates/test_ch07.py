import unittest

import ch07_examples as ex


class TestChapter7(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual((ex.steps("log n", 1), ex.steps("n log n", 1), ex.steps("2^n", 1), ex.steps("n^2", 1)), (0, 0, 2, 1))
        self.assertEqual((ex.steps("n^2", 2), ex.steps("2^n", 2)), (4, 4))
        self.assertLess(ex.steps("2^n", 3), ex.steps("n^2", 3))
        self.assertEqual((ex.steps("n^2", 4), ex.steps("2^n", 4)), (16, 16))
        for n in range(5, 40):
            self.assertGreater(ex.steps("2^n", n), ex.steps("n^2", n))
        self.assertLess(ex.steps("n^3", 10), ex.steps("2^n", 10))
        self.assertEqual([ex.halvings(n) for n in (0, 1, 2, 3, 16, 17, 1_000_000)], [0, 0, 1, 1, 4, 4, 19])
        self.assertEqual(ex.grains_on_square(64), 9_223_372_036_854_775_808)
        self.assertEqual([ex.largest_n(r) for r in ("n", "n log n", "n^2", "n^3", "2^n")],
                         [10_000_000, 526_172, 3_162, 215, 23])

    def test_one_second(self) -> None:
        self.assertEqual([ex.largest_n(r) for r in ("n", "n log n", "n^2", "n^3", "2^n")],
                         [10_000_000, 526_172, 3_162, 215, 23])
        self.assertEqual(ex.largest_n("2^n", 1e8), 26)

    def test_small_facts(self) -> None:
        self.assertEqual(ex.halvings(16), 4)
        self.assertEqual(ex.halvings(1_000_000), 19)
        self.assertEqual(ex.halvings(1000), 9)
        self.assertEqual(ex.grains_on_square(11), 1024)
        self.assertEqual(sum(ex.grains_on_square(k) for k in range(1, 11)), 1023)
        self.assertAlmostEqual(ex.steps("n log n", 1024), 10240)
        self.assertEqual(ex.steps("n^2", 4000) // 2 // 1e6, 8)


if __name__ == "__main__":
    unittest.main()
