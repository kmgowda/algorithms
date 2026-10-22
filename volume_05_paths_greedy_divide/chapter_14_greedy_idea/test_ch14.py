import unittest

import ch14_examples as ex


class TestChapter13(unittest.TestCase):
    def test_change(self) -> None:
        self.assertEqual(ex.greedy_change(87, ex.UK), [50, 20, 10, 5, 2])
        self.assertEqual(len(ex.fewest_coins(87, ex.UK)), 5)
        self.assertEqual((ex.greedy_change(6, ex.ODD), sorted(ex.fewest_coins(6, ex.ODD))), ([4, 1, 1], [3, 3]))
        self.assertEqual([ex.first_failure(c) for c in (ex.UK, ex.ODD, [25, 10, 1])], [None, 6, 30])

    def test_every_case(self) -> None:
        self.assertEqual((ex.greedy_change(0, ex.UK), ex.fewest_coins(0, ex.UK)), ([], []))
        self.assertEqual(ex.greedy_change(7, [5, 2]), [5, 2])
        with self.assertRaises(ValueError):
            ex.greedy_change(3, [5, 2])
        self.assertIsNone(ex.fewest_coins(3, [5, 2]))
        self.assertEqual(len(ex.greedy_change(30, [25, 10, 1])), 6)
        self.assertEqual(ex.greedy_change(399, ex.UK), [200, 100, 50, 20, 20, 5, 2, 2])
        self.assertEqual((ex.first_failure([12, 5, 1]), ex.first_failure([10, 5, 1])), (15, None))
        self.assertEqual(ex.greedy_change(63, ex.UK), [50, 10, 2, 1])
        with self.assertRaises(ValueError):
            ex.greedy_change(6, [5, 2])                                        # greedy is stuck, yet 2 + 2 + 2 works
        self.assertEqual(ex.fewest_coins(6, [5, 2]), [2, 2, 2])
        self.assertEqual(len(ex.fewest_coins(399, ex.UK)), 8)

    def test_practice(self) -> None:
        self.assertEqual((ex.first_failure([10, 7, 1]), ex.greedy_change(14, [10, 7, 1])), (14, [10, 1, 1, 1, 1]))
        self.assertEqual(ex.fewest_coins(14, [10, 7, 1]), [7, 7])
        self.assertEqual([ex.largest_smaller_total([8, 4, 2, 1], c, 60)[0] for c in (2, 4, 8)], [1, 3, 7])
        self.assertIsNone(ex.first_failure([8, 4, 2, 1]))
        self.assertIsNone(ex.first_failure([9, 1]))

    def test_smaller_coins(self) -> None:
        got = [ex.largest_smaller_total(ex.UK, c, 300)[0] for c in (2, 5, 10, 20, 50, 100, 200)]
        self.assertEqual(got, [1, 4, 9, 19, 49, 99, 199])
        self.assertEqual(ex.largest_smaller_total(ex.UK, 50, 300)[1], [20, 20, 5, 2, 2])
        self.assertEqual(ex.largest_smaller_total(ex.ODD, 4, 50), (9, [3, 3, 3]))
        self.assertEqual(ex.largest_smaller_total(ex.UK, 1, 10), (0, []))       # nothing is smaller than 1p
        self.assertEqual(ex.largest_smaller_total([25, 10, 1], 25, 100)[0], 44)  # 44 >= 25: greed is not safe


if __name__ == "__main__":
    unittest.main()
