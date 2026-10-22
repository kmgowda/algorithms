import random
import unittest

import ch21_examples as ex
import ch21_solutions as sol


class TestCountDivisible(unittest.TestCase):
    def test_smallest(self) -> None:
        self.assertEqual(sol.count_divisible([], 3), 0)
        self.assertEqual(sol.count_divisible([4], 1), 1)
        self.assertEqual(sol.count_divisible([4], 2), 1)
        self.assertEqual(sol.count_divisible([3], 2), 0)

    def test_visits(self) -> None:
        self.assertEqual(sol.count_divisible(ex.VISITS, 5), 11)
        self.assertEqual(sol.count_divisible(ex.VISITS, 1), 55)

    def test_random_and_pigeonhole(self) -> None:
        rng = random.Random(21)
        for _ in range(500):
            v = [rng.randint(-9, 9) for _ in range(rng.randint(0, 12))]
            k = rng.randint(1, 7)
            brute = sum(sum(v[i:j]) % k == 0 for i in range(len(v)) for j in range(i + 1, len(v) + 1))
            self.assertEqual(sol.count_divisible(v, k), brute)
            if v:
                self.assertGreaterEqual(sol.count_divisible(v, len(v)), 1)    # Thinking Problem 1


class TestGridBookings(unittest.TestCase):
    def test_bug(self) -> None:
        self.assertEqual(sol.grid_bookings([(0, 0, 0, 0, 1)], 3, 3, marks=2), [[1, 1, 1], [1, 0, 0], [1, 0, 0]])
        self.assertEqual(sol.grid_bookings([(0, 0, 0, 0, 1)], 3, 3), [[1, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_random(self) -> None:
        rng = random.Random(3)
        self.assertEqual(sol.grid_bookings([], 0, 0), [])
        for _ in range(200):
            rows, cols = rng.randint(1, 5), rng.randint(1, 5)
            bk = []
            for _ in range(rng.randint(0, 4)):
                r1 = rng.randrange(rows); r2 = rng.randrange(r1, rows)
                c1 = rng.randrange(cols); c2 = rng.randrange(c1, cols)
                bk.append((r1, c1, r2, c2, rng.randint(1, 3)))
            direct = [[sum(c for a, b, x, y, c in bk if a <= r <= x and b <= q <= y) for q in range(cols)]
                      for r in range(rows)]
            self.assertEqual(sol.grid_bookings(bk, rows, cols), direct)


class TestExamWeek(unittest.TestCase):
    def test_week_against_direct(self) -> None:
        rng = random.Random(1)
        week = [(a, min(97, a + rng.randint(0, 5)), rng.randint(1, 4)) for a in (rng.randrange(98) for _ in range(2000))]
        direct = [sum(c for a, b, c in week if a <= h <= b) for h in range(98)]
        self.assertEqual(ex.chairs_in_use(week, 98), direct)
        self.assertEqual(sum(b - a + 1 for a, b, c in week), 6939)


if __name__ == "__main__":
    unittest.main()
