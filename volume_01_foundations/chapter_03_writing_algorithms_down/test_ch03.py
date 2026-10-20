import math
import unittest

import ch03_examples as ex


class TestChapter3(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
