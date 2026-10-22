import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_every_case(self) -> None:
        for target, want in [(30, (3, 5)), (10, (0, 1)), (37, (5, 6)), (26, (1, 6)), (8, None), (100, None)]:
            self.assertEqual((ex.pair_brute(ex.PRICES, target), ex.pair_two_pointers(ex.PRICES, target)), (want, want))
        self.assertEqual((ex.pair_two_pointers([], 5), ex.pair_two_pointers([7], 14)), (None, None))
        self.assertEqual(ex.pair_two_pointers([7, 7], 14), (0, 1))
        self.assertEqual((ex.pair_brute([13, 4, 9], 13), ex.pair_two_pointers([13, 4, 9], 13)), ((1, 2), None))

    def test_examples(self) -> None:
        self.assertEqual(ex.pair_two_pointers(ex.PRICES, 30), (3, 5))
        self.assertEqual(ex.pair_brute(ex.PRICES, 30), (3, 5))
        self.assertEqual(ex.pair_two_pointers(ex.PRICES, 35), (4, 6))
        self.assertEqual(ex.pair_two_pointers(ex.PRICES, 24), (0, 6))
        self.assertIsNone(ex.pair_two_pointers(ex.PRICES, 100))
        self.assertIsNone(ex.pair_two_pointers([4, 13, 20], 26))
        self.assertIsNone(ex.pair_two_pointers([], 5))
        self.assertIsNone(ex.pair_two_pointers([5], 10))

    def test_random_against_brute(self) -> None:
        rng = random.Random(7)
        for _ in range(2000):
            prices = sorted(rng.randint(1, 30) for _ in range(rng.randint(0, 12)))
            self.assertTrue(ex.agree(prices, rng.randint(0, 60)))

    def test_zigzag_practice(self) -> None:
        self.assertEqual(ex.pair_two_pointers(ex.PRICES, 22), (2, 3))
        self.assertEqual(ex.pair_brute(ex.PRICES, 22), (2, 3))


if __name__ == "__main__":
    unittest.main()
