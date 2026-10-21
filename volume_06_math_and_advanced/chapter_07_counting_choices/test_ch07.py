import itertools
import math
import unittest

import ch07_examples as ex


class TestChapter7(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.orders(5), ex.arrangements(10, 3), ex.choose(10, 3), ex.choose(52, 5)), (120, 720, 120, 2598960))
        self.assertEqual((ex.choose_mod(1000, 500), len(str(ex.choose(1000, 500)))), (159835829, 300))
        self.assertEqual((ex.with_repetition(3, 4), sum(ex.choose(10, k) for k in range(11))), (15, 1024))

    def test_every_case(self) -> None:
        self.assertEqual((ex.orders(0), ex.choose(5, 0), ex.choose(5, 5), ex.choose(5, 6), ex.choose_mod(5, 6), ex.choose_mod(0, 0)), (1, 1, 1, 0, 0, 1))
        self.assertEqual((ex.arrangements(5, 0), ex.with_repetition(0, 0), ex.with_repetition(0, 3), ex.with_repetition(3, 0)), (1, 1, 0, 1))
        for n in range(8):
            for k in range(n + 2):
                self.assertEqual(ex.choose(n, k), len(list(itertools.combinations(range(n), k))))
                self.assertEqual(ex.choose_mod(n, k), ex.choose(n, k) % ex.P)
            for k in range(5):
                self.assertEqual(ex.with_repetition(n, k), len(list(itertools.combinations_with_replacement(range(n), k))))


if __name__ == "__main__":
    unittest.main()
