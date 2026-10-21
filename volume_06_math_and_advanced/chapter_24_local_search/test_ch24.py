import random
import unittest

import ch24_examples as ex


class TestChapter24(unittest.TestCase):
    def test_examples(self) -> None:
        pts = ex.places(12, 1)
        start = list(range(12))
        t2, moves = ex.two_opt(start, pts)
        ta = ex.annealing(start, pts, random.Random(24))
        self.assertEqual((round(ex.length(start, pts), 1), round(ex.length(t2, pts), 1), moves, round(ex.length(ta, pts), 1), round(ex.exact(pts), 1)),
                         (687.8, 397.4, 11, 391.9, 391.9))
        stuck = [round(ex.length(ex.two_opt(random.Random(s).sample(range(12), 12), pts)[0], pts), 1) for s in range(10)]
        self.assertEqual(stuck.count(391.9), 3)

    def test_every_case(self) -> None:
        pts = ex.places(12, 1)
        self.assertEqual((ex.length([0], pts), ex.two_opt([0, 1], pts), ex.two_opt([0, 1, 2], pts)[1]), (0.0, ([0, 1], 0), 0))
        for s in range(5):
            t = random.Random(s).sample(range(8), 8)
            self.assertEqual(sorted(ex.two_opt(t, pts[:8])[0]), list(range(8)))
            self.assertGreaterEqual(round(ex.length(ex.two_opt(t, pts[:8])[0], pts), 6), round(ex.exact(pts[:8]), 6))


if __name__ == "__main__":
    unittest.main()
