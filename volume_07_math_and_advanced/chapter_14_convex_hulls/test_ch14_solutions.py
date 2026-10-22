import itertools
import math
import random
import unittest

import ch14_examples as ex
import ch14_solutions as sol


def brute(points) -> float:
    """Try the normal of every pair of points as the strip's direction: O(n^3)."""
    pts = sorted(set(points))
    best = math.inf if len(ex.convex_hull(pts)) >= 3 else 0.0
    for p, q in itertools.combinations(pts, 2):
        u = (q[1] - p[1], p[0] - q[0])
        proj = [(u[0] * x + u[1] * y) / math.hypot(*u) for x, y in pts]
        best = min(best, max(proj) - min(proj))
    return best


class TestMinWidth(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.min_width([]), 0.0)
        self.assertEqual(sol.min_width([(3, 4)]), 0.0)
        self.assertEqual(sol.min_width([(0, 0), (2, 2), (5, 5)]), 0.0)
        self.assertAlmostEqual(sol.min_width([(0, 0), (4, 0), (0, 3)]), 2.4)       # height onto the long side
        self.assertAlmostEqual(sol.min_width([(0, 0), (6, 0), (6, 2), (0, 2), (3, 1)]), 2.0)

    def test_drop_boxes(self) -> None:
        self.assertAlmostEqual(sol.min_width(ex.BOXES), brute(ex.BOXES))

    def test_against_brute_force(self) -> None:
        r = random.Random(14)
        for _ in range(300):
            pts = [(r.randint(0, 9), r.randint(0, 9)) for _ in range(r.randint(0, 9))]
            self.assertAlmostEqual(sol.min_width(pts), brute(pts), msg=str(pts))


if __name__ == "__main__":
    unittest.main()
