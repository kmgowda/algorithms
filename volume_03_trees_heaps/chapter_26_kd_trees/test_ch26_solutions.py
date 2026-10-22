import math
import random
import unittest

import ch26_examples as ex
import ch26_solutions as sol


class TestChapter26Solutions(unittest.TestCase):
    def test_median_height(self) -> None:
        self.assertEqual(sol.median_height(0), -1)
        for n in range(1, 300):
            self.assertEqual(sol.median_height(n), int(math.log2(n)))

    def test_range_count(self) -> None:
        t = ex.KDTree(ex.BRANCHES.values())
        self.assertEqual(sol.range_count(t, (6, 3), (9, 9)), 2)
        t.visited = 0
        self.assertEqual(sol.range_count(t, (0, 0), (10, 10)), 9)
        self.assertEqual(t.visited, 9)                             # the outer regions are unbounded, never inside
        self.assertEqual(sol.range_count(ex.KDTree(), (0, 0), (1, 1)), 0)    # empty tree
        self.assertEqual(sol.range_count(ex.KDTree([(2, 2)]), (2, 2), (2, 2)), 1)
        self.assertEqual(sol.range_count(t, (5, 5), (4, 4)), 0)    # backwards box
        rng = random.Random(3)
        for trial in range(250):
            pts = [(rng.randrange(10), rng.randrange(10)) for _ in range(rng.randrange(0, 50))]
            t = ex.KDTree(pts)
            lo = (rng.randrange(-1, 10), rng.randrange(-1, 10))
            hi = (lo[0] + rng.randrange(0, 6), lo[1] + rng.randrange(0, 6))
            self.assertEqual(sol.range_count(t, lo, hi), len(ex.brute_range(pts, lo, hi)))
        big = ex.KDTree(ex.random_points(16384, seed=3))
        big.visited = 0
        self.assertEqual(sol.range_count(big, (0.2, 0.2), (0.8, 0.8)), 5877)
        self.assertEqual(big.visited, 911)                         # listing them opens 6,233 nodes

    def test_far_child_rule_fails(self) -> None:
        t = ex.KDTree(ex.BRANCHES.values())
        self.assertEqual(sol.nearest_far_child_rule(t, (1, 7)), ((3, 7), 4))   # Castle, but Abbey is 1 away
        self.assertEqual(t.nearest((1, 7)), ((1, 6), 1))
        self.assertEqual(sol.nearest_far_child_rule(ex.KDTree(), (0, 0)), (None, math.inf))


if __name__ == "__main__":
    unittest.main()
