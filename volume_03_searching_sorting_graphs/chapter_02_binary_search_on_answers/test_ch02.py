import math
import random
import unittest

import ch02_examples as ex


class TestChapter02(unittest.TestCase):
    def test_trolley(self) -> None:
        t = []
        self.assertEqual(ex.smallest_capacity(ex.BOXES, 3, t), 16)
        self.assertEqual(t, [(9, 44, 26, True), (9, 26, 17, True), (9, 17, 13, False), (14, 17, 15, False),
                             (16, 17, 16, True)])
        self.assertEqual([ex.smallest_capacity(ex.BOXES, k) for k in (2, 3, 4, 8)], [24, 16, 14, 9])
        self.assertEqual(ex.loads(ex.BOXES, 16), [[5, 9], [3, 7, 4], [8, 2, 6]])

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            boxes = [rng.randint(1, 20) for _ in range(rng.randint(1, 12))]
            for k in range(1, len(boxes) + 1):
                self.assertEqual(ex.smallest_capacity(boxes, k), ex.brute_capacity(boxes, k))

    def test_every_case(self) -> None:
        table = [(ex.BOXES, 8, 9, 6), (ex.BOXES, 1, 44, 5), (ex.BOXES, 3, 16, 5), ([7], 1, 7, 0), ([5, 5, 5, 5], 2, 10, 4)]
        for boxes, trips, answer, checks in table:
            t = []
            self.assertEqual(ex.smallest_capacity(boxes, trips, t), answer)
            self.assertEqual(len(t), checks)

    def test_reading_speed(self) -> None:
        books = [300, 120, 450, 210]
        s = ex.slowest_reading_speed(books, 8)
        self.assertEqual(s, 150)
        self.assertLessEqual(sum(math.ceil(p / s) for p in books), 8)
        self.assertGreater(sum(math.ceil(p / (s - 1)) for p in books), 8)

    def test_last_true(self) -> None:
        t = []
        self.assertEqual(ex.longest_piece([8, 5, 11], 5, t), 4)
        self.assertEqual(t, [(1, 11, 6, False), (1, 5, 3, True), (3, 5, 4, True), (4, 5, 5, False)])
        self.assertEqual(ex.last_true_rounding_down(1, 11, lambda L: ex.pieces([8, 5, 11], L) >= 5), (4, 5, 20))
        self.assertEqual(ex.longest_piece([8, 5, 11], 100), 0)      # impossible: not even 1-metre pieces
        self.assertEqual(ex.longest_piece([7], 1), 7)                # one rope, one piece
        self.assertEqual(ex.last_true(3, 3, lambda x: True), 3)      # a range of one value
        rng = random.Random(2)
        for _ in range(200):
            ropes = [rng.randint(1, 30) for _ in range(rng.randint(1, 6))]
            k = rng.randint(1, 20)
            best = max([L for L in range(1, 31) if ex.pieces(ropes, L) >= k], default=0)
            self.assertEqual(ex.longest_piece(ropes, k), best)

    def test_widest_spacing(self) -> None:
        self.assertEqual(ex.widest_spacing([1, 2, 4, 8, 9], 3), 3)
        self.assertEqual(ex.widest_spacing([0, 10], 2), 10)
        self.assertEqual(ex.widest_spacing([3, 4, 5], 3), 1)
        rng = random.Random(3)
        for _ in range(100):
            desks = sorted(rng.sample(range(40), rng.randint(2, 8)))
            k = rng.randint(2, len(desks))
            best = max(g for g in range(1, 41) if ex.lamps_fit(desks, k, g))
            self.assertEqual(ex.widest_spacing(desks, k), best)

    def test_real_threshold(self) -> None:
        r = ex.real_threshold(1.0, 2.0, lambda m: m * m >= 2, 20)
        self.assertTrue(r * r >= 2)
        self.assertLess(r - math.sqrt(2), 2 ** -20)
        self.assertEqual(ex.real_threshold(1.0, 2.0, lambda m: True, 0), 2.0)


if __name__ == "__main__":
    unittest.main()
