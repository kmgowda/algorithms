import math
import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_formulas(self) -> None:
        self.assertTrue(all(ex.check_formulas(n) for n in range(1, 400)))
        self.assertEqual(ex.gauss_sum(100), 5050)
        self.assertEqual(ex.powers_of_two_sum(10), 1023)
        self.assertEqual(ex.halving_total(1000), 1994)
        for s in range(1, 3000):
            self.assertLess(ex.halving_total(s), 2 * s)
        self.assertEqual((math.floor(math.log2(100)), math.ceil(math.log2(100))), (6, 7))


if __name__ == "__main__":
    unittest.main()
