import unittest

import ch13_examples as ex


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


if __name__ == "__main__":
    unittest.main()
