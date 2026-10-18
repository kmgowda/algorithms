import math
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestPrefix(unittest.TestCase):
    def test_range_totals(self) -> None:
        rng = random.Random(1)
        v = [rng.randint(-50, 50) for _ in range(30)]
        rt = ex.RangeTotals(v)
        for _ in range(300):
            i = rng.randrange(30)
            j = rng.randrange(i, 30)
            self.assertEqual(rt.total(i, j), sum(v[i:j + 1]))
        with self.assertRaises(IndexError):
            rt.total(5, 30)

    def test_balance_and_products(self) -> None:
        self.assertEqual(ex.balance_point([1, 7, 3, 6, 5, 6]), 3)
        self.assertEqual(ex.balance_point([1, 2, 3]), -1)
        self.assertEqual(ex.balance_point([2, 1, -1]), 0)
        rng = random.Random(2)
        for _ in range(200):
            v = [rng.randint(-3, 3) for _ in range(rng.randint(1, 8))]
            self.assertEqual(ex.product_of_others(v), [math.prod(v[:i] + v[i + 1:]) for i in range(len(v))])

    def test_difference_array(self) -> None:
        rng = random.Random(3)
        for _ in range(200):
            n = rng.randint(1, 15)
            updates = []
            for _ in range(rng.randint(0, 6)):
                a = rng.randrange(n)
                b = rng.randrange(a, n)
                updates.append((a, b, rng.randint(-5, 5)))
            brute = [0] * n
            for a, b, amt in updates:
                for k in range(a, b + 1):
                    brute[k] += amt
            self.assertEqual(ex.apply_range_updates(n, updates), brute)

    def test_hotel_and_museum(self) -> None:
        self.assertEqual(ex.hotel_occupancy([(0, 2), (1, 3), (2, 2), (4, 5)], 6), [1, 2, 3, 1, 1, 1])
        self.assertEqual(ex.busiest_hour([(9, 12), (10, 11), (10, 13), (14, 16)]), (10, 3))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.running_totals([3, 1, 4, 1]), [3, 4, 8, 9])
        self.assertEqual(sol.flight_bookings([(1, 2, 10), (2, 3, 20), (2, 5, 25)], 5), [10, 55, 45, 25, 25])
        self.assertFalse(sol.car_pooling([(2, 1, 5), (3, 3, 7)], 4))
        self.assertTrue(sol.car_pooling([(2, 1, 5), (3, 3, 7)], 5))
        self.assertTrue(sol.car_pooling([(2, 1, 5), (3, 5, 7)], 3))
        self.assertTrue(sol.car_pooling([], 1))
        self.assertEqual(sol.count_in_ranges([5, 12, 30, 18, 2], [(0, 4), (1, 3)], 10, 20), [2, 2])


if __name__ == "__main__":
    unittest.main()
