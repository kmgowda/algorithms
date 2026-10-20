import unittest

import ch17_examples as ex


class TestChapter17(unittest.TestCase):
    def test_doubling(self) -> None:
        for n in range(1, 3000):
            costs = ex.append_costs(n)
            self.assertLess(sum(costs), 3 * n)
            self.assertLess(sum(costs) - n, 2 * n)
        c = ex.append_costs(33)
        self.assertEqual([i + 1 for i, x in enumerate(c) if x > 1], [2, 3, 5, 9, 17, 33])
        self.assertEqual(sum(c), 96)
        self.assertEqual(sum(ex.append_costs(16)), 31)
        self.assertEqual(sum(ex.append_costs(17)), 48)
        self.assertEqual(sum(ex.append_costs(10_000)) - 10_000, 16_383)

    def test_fixed_growth(self) -> None:
        self.assertEqual(ex.copying_with_fixed_growth(10_000), 4_995_000)


if __name__ == "__main__":
    unittest.main()
