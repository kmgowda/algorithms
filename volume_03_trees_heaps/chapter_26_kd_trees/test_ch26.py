import math
import random
import unittest

import ch26_examples as ex


class TestChapter26(unittest.TestCase):
    def test_branches(self) -> None:
        t = ex.KDTree(ex.BRANCHES.values())
        self.assertTrue(t.valid())
        self.assertEqual(t.height(), 3)
        self.assertEqual(t.root.point, (5, 4))                    # Market: the median by x
        self.assertEqual((t.root.left.point, t.root.right.point), ((3, 7), (8, 5)))
        self.assertEqual(sorted(t.range_search(*ex.BOX)), [(7, 8), (8, 5)])
        self.assertEqual(t.visited, 5)                            # the four western branches are skipped
        t.visited = 0
        self.assertEqual(t.nearest(ex.READER), ((8, 5), 2))       # Wharf
        self.assertEqual(t.visited, 5)
        self.assertEqual([p for p, _, _ in ex.nearest_trace(t, ex.READER)], [(5, 4), (8, 5), (9, 2), (6, 1), (7, 8)])

    def test_every_case(self) -> None:
        t = ex.KDTree()                                           # empty tree
        self.assertEqual(t.nearest((1, 1)), (None, math.inf))
        self.assertEqual(t.range_search((0, 0), (9, 9)), [])
        self.assertFalse(t.delete((1, 1)))
        t.insert((3, 3))                                          # one point
        self.assertEqual(t.nearest((9, 9)), ((3, 3), 72))
        self.assertTrue(t.delete((3, 3)))
        self.assertIsNone(t.root)
        b = ex.KDTree(ex.BRANCHES.values())
        self.assertEqual(b.nearest((5, 4)), ((5, 4), 0))          # the query is a branch
        self.assertEqual(sorted(b.range_search((5, 0), (5, 9))), [(5, 4)])   # a box on the splitting line
        self.assertEqual(sorted(b.range_search((0, 0), (10, 10))), sorted(ex.BRANCHES.values()))
        self.assertEqual(b.range_search((6, 6), (6, 7)), [])      # a box holding no branch
        self.assertEqual(b.range_search((7, 3), (6, 9)), [])      # a backwards box
        self.assertEqual(b.nearest((40, 40)), ((7, 8), 33 ** 2 + 32 ** 2))   # far outside every point
        tie = ex.KDTree([(0, 0), (2, 0), (1, 5)])                 # a tie: (1, 0) is 1 from both
        self.assertEqual(tie.nearest((1, 0))[1], 1)
        tie = ex.KDTree([(3, 3), (5, 3), (4, 8)])                 # Figure 26.6, panel 5
        self.assertEqual(tie.nearest((4, 3)), ((5, 3), 1))        # the first one found is kept
        d = ex.KDTree([(4, 4), (4, 4), (4, 4), (4, 1)])           # duplicates
        self.assertTrue(d.valid())
        self.assertEqual(len(d.range_search((4, 4), (4, 4))), 3)
        self.assertTrue(d.delete((4, 4)))
        self.assertEqual(sorted(d.points()), [(4, 1), (4, 4), (4, 4)])
        self.assertTrue(d.valid())
        path = ex.KDTree()                                        # sorted insertions make a path
        for i in range(8):
            path.insert((i, i))
        self.assertEqual(path.height(), 7)
        self.assertTrue(path.valid())

    def test_random_against_brute_force(self) -> None:
        rng = random.Random(26)
        for trial in range(250):
            dims = 2 if trial % 3 else 3
            pts = [tuple(rng.randrange(8) for _ in range(dims)) for _ in range(rng.randrange(0, 40))]
            t = ex.KDTree(pts[: len(pts) // 2], dims)
            for p in pts[len(pts) // 2:]:
                t.insert(p)
            for _ in range(rng.randrange(0, 8)):
                if pts:
                    p = pts.pop(rng.randrange(len(pts)))
                    self.assertTrue(t.delete(p))
            self.assertFalse(t.delete((99,) * dims))
            self.assertTrue(t.valid())
            self.assertEqual(sorted(t.points()), sorted(pts))
            for _ in range(8):
                q = tuple(rng.randrange(-2, 10) for _ in range(dims))
                self.assertEqual(t.nearest(q)[1], ex.brute_nearest(pts, q))
                lo = tuple(rng.randrange(-1, 9) for _ in range(dims))
                hi = tuple(c + rng.randrange(0, 5) for c in lo)
                self.assertEqual(sorted(t.range_search(lo, hi)), ex.brute_range(pts, lo, hi))

    def test_measurements(self) -> None:
        self.assertEqual(ex.line_cost(16384), 254.0)                # about 2 sqrt(n) regions
        t = ex.KDTree(ex.random_points(4096))
        self.assertEqual(t.height(), 12)
        self.assertLess(ex.nearest_cost(10_000, 2), 25)
        self.assertGreater(ex.nearest_cost(10_000, 16, queries=20), 5000)   # high dimensions: most of the tree


if __name__ == "__main__":
    unittest.main()
