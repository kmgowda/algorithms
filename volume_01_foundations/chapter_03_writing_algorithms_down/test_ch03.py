import math
import unittest

import ch03_examples as ex


class TestChapter3(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([ex.shelf_for(n) for n in (0, 29, 30, 59, 60, 91)], ["A", "A", "B", "B", "C", "C"])
        self.assertEqual([ex.count_above(ex.SHELF, k) for k in (5, 58, 91, 95)], [9, 4, 0, 0])
        self.assertEqual(ex.count_above([], 50), 0)
        self.assertEqual([ex.halving_rounds(b) for b in (0, 1, 2, 3, 8, 9, 100)], [0, 0, 1, 1, 3, 3, 6])
        self.assertEqual([ex.late_fee(d) for d in (0, 2, 3, 12, 13, 40)], [0, 0, 10, 100, 100, 100])
        self.assertEqual(ex.swap(5, 5), (5, 5))

    def test_rules(self) -> None:
        self.assertEqual([ex.shelf_for(n) for n in (29, 30, 59, 60)], ["A", "B", "B", "C"])
        self.assertEqual(ex.count_above(ex.SHELF, 50), 5)
        self.assertEqual(ex.count_above(ex.SHELF, 60), 4)
        self.assertEqual([ex.late_fee(d) for d in (4, 12, 2, 13, 0)], [20, 100, 0, 100, 0])
        self.assertEqual(ex.swap(3, 8), (8, 3))

    def test_halving(self) -> None:
        self.assertEqual(ex.halving_rounds(9), 3)
        self.assertEqual(ex.halving_rounds(100), 6)
        for n in range(1, 5000):
            self.assertEqual(ex.halving_rounds(n), int(math.log2(n)))


    def test_close_pairs(self) -> None:
        self.assertEqual(ex.close_pairs(ex.SHELF, 10), ([(25, 31), (58, 63), (63, 70), (84, 91)], 36))
        self.assertEqual(ex.close_pairs([], 10), ([], 0))
        self.assertEqual(ex.close_pairs([5], 10), ([], 0))
        self.assertEqual(ex.close_pairs(ex.SHELF, 0), ([], 36))

if __name__ == "__main__":
    unittest.main()
