import random
import unittest

import ch25_examples as ex
import ch25_solutions as sol


class TestChapter25Solutions(unittest.TestCase):
    def test_first_overlap(self) -> None:
        t = ex.IntervalTree(ex.BOOKINGS)
        self.assertEqual(t.find_overlap(14, 17).interval(), (12, 15))   # the claim of Thinking Problem 1 fails
        self.assertEqual(sol.first_overlap(t, 14, 17).interval(), (9, 14))
        self.assertIsNone(sol.first_overlap(ex.IntervalTree(), 1, 2))   # empty tree
        self.assertIsNone(sol.first_overlap(t, 19, 19))
        self.assertIsNone(sol.first_overlap(t, 5, 4))
        one = ex.IntervalTree([(2, 3)])
        self.assertEqual(sol.first_overlap(one, 3, 9).interval(), (2, 3))
        rng = random.Random(1)
        for trial in range(300):
            data = ex.random_bookings(rng.randrange(0, 30), days=50, longest=12, seed=trial)
            t = ex.IntervalTree(data)
            lo, hi = sorted(rng.sample(range(-2, 55), 2))
            want = ex.brute_overlaps(data, lo, hi)
            got = sol.first_overlap(t, lo, hi)
            self.assertEqual(got and got.interval(), want[0] if want else None)

    def test_covering(self) -> None:
        t = ex.IntervalTree(ex.BOOKINGS)
        self.assertEqual(sol.covering(t, 16, 17).interval(), (16, 18))
        self.assertIsNone(sol.covering(t, 13, 16))
        self.assertEqual(sol.covering(t, 10, 11).interval(), (9, 14))
        self.assertIsNone(sol.covering(ex.IntervalTree(), 1, 1))        # empty tree
        self.assertIsNone(sol.covering(t, 9, 8))                        # backwards query
        self.assertEqual(sol.covering(ex.IntervalTree([(4, 4)]), 4, 4).interval(), (4, 4))
        rng = random.Random(2)
        for trial in range(400):
            data = ex.random_bookings(rng.randrange(0, 30), days=40, longest=15, seed=trial)
            t = ex.IntervalTree(data) if trial % 2 else ex.IntervalTree.balanced(data)
            lo = rng.randrange(-2, 45)
            hi = lo + rng.randrange(0, 6)
            want = sol.brute_covering(data, lo, hi)
            t.visited = 0
            got = sol.covering(t, lo, hi)
            self.assertEqual(got is None, not want)
            if got:
                self.assertIn(got.interval(), want)
            self.assertLessEqual(t.visited, 2 * (t.height() + 1))

    def test_spread_example(self) -> None:
        self.assertEqual(sol.spread_example(1023, 32), (160, 9, 32))
        self.assertEqual(sol.spread_example(65535, 1024), (6144, 15, 1024))
        self.assertEqual(sol.spread_example(1, 1), (1, 0, 1))


if __name__ == "__main__":
    unittest.main()
