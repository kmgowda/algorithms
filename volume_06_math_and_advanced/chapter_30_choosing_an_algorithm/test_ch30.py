import unittest

import ch30_examples as ex


class TestChapter30(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual([ex.largest_input(r, 10 ** 8) for r in ex.GROWTH], [100000000, 4523071, 10000, 464, 26, 11])
        self.assertEqual(ex.advise("sub-problems repeat"), [("dynamic programming", "Volume 5, Part I")])
        self.assertEqual(ex.advise("routes on a map")[0][1], "Volume 4, Part I")

    def test_every_case(self) -> None:
        self.assertEqual((ex.largest_input("n", 0), ex.largest_input("n", 1), ex.largest_input("2^n", 1)), (0, 1, 0))
        self.assertEqual((ex.advise(""), ex.advise("banana")), ([], []))
        for rate, f in ex.GROWTH.items():
            n = ex.largest_input(rate, 10 ** 6)
            self.assertLessEqual(f(n), 10 ** 6)
            self.assertGreater(f(n + 1), 10 ** 6)


if __name__ == "__main__":
    unittest.main()
