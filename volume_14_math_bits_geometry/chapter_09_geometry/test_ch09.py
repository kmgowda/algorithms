import itertools
import random
import unittest
from fractions import Fraction

import ch09_examples as ex
import ch09_solutions as sol


def brute_intersect(a, b, c, d):
    """Exact check with fractions: solve a + t(b - a) = c + s(d - c), or handle collinear overlap."""
    r = (b[0] - a[0], b[1] - a[1])
    s = (d[0] - c[0], d[1] - c[1])
    den = r[0] * s[1] - r[1] * s[0]
    qp = (c[0] - a[0], c[1] - a[1])
    if den == 0:
        if qp[0] * r[1] - qp[1] * r[0] != 0:
            return False                                   # parallel, not on one line
        return any(ex.on_segment(p, x, y) for p, x, y in ((a, c, d), (b, c, d), (c, a, b), (d, a, b)))
    t = Fraction(qp[0] * s[1] - qp[1] * s[0], den)
    u = Fraction(qp[0] * r[1] - qp[1] * r[0], den)
    return 0 <= t <= 1 and 0 <= u <= 1


class TestGeometry(unittest.TestCase):
    def test_hull_and_area(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            pts = [(rng.randint(0, 10), rng.randint(0, 10)) for _ in range(rng.randint(1, 15))]
            hull = ex.convex_hull(pts)
            self.assertTrue(set(hull) <= set(pts))
            if len(hull) >= 3:
                for i in range(len(hull)):
                    self.assertGreater(ex.cross(hull[i - 2], hull[i - 1], hull[i]), 0)
                for p in pts:
                    self.assertTrue(all(ex.cross(hull[i - 1], hull[i], p) >= 0 for i in range(len(hull))))
                    self.assertIn(ex.point_in_polygon(p, hull), ("inside", "boundary"))
                cells = sum(1 for x in range(11) for y in range(11) if ex.point_in_polygon((x, y), hull) == "inside")
                boundary = sum(1 for x in range(11) for y in range(11) if ex.point_in_polygon((x, y), hull) == "boundary")
                self.assertEqual(ex.polygon_area(hull), cells + boundary / 2 - 1)        # Pick's theorem
            if len(hull) >= 3:
                on_fence = {q for q in pts if any(ex.on_segment(q, hull[i - 1], hull[i]) for i in range(len(hull)))}
                self.assertEqual(set(sol.fence_trees(pts)), on_fence)
            self.assertEqual(sol.hull_size(pts), len(hull))
            best = max((sum(1 for p in pts if ex.cross(a, b, p) == 0) for a, b in itertools.combinations(pts, 2) if a != b),
                       default=len(pts))
            if len(set(pts)) == len(pts):
                self.assertEqual(sol.max_points_on_line(pts), best if len(pts) > 2 else len(pts))

    def test_intersections(self) -> None:
        rng = random.Random(2)
        for _ in range(2000):
            a, b, c, d = [(rng.randint(0, 5), rng.randint(0, 5)) for _ in range(4)]
            self.assertEqual(ex.segments_intersect(a, b, c, d), brute_intersect(a, b, c, d), (a, b, c, d))

    def test_examples(self) -> None:
        self.assertEqual(ex.orientation((0, 0), (4, 0), (4, 3)), "left")
        self.assertEqual(ex.polygon_area([(0, 0), (4, 0), (4, 3), (0, 3)]), 12)
        self.assertEqual(ex.convex_hull([(0, 0), (2, 1), (4, 0), (3, 2), (4, 4), (1, 3), (0, 4), (2, 2)]),
                         [(0, 0), (4, 0), (4, 4), (0, 4)])
        hull, area, per = ex.delivery_zone([(1, 1), (6, 2), (5, 7), (2, 6), (3, 3), (4, 4)])
        self.assertEqual(area, 20.0)
        self.assertTrue(sol.is_convex([(0, 0), (4, 0), (4, 4), (0, 4)]))
        self.assertFalse(sol.is_convex([(0, 0), (4, 0), (1, 1), (0, 4)]))
        self.assertEqual(sol.fence_trees([(1, 1), (2, 2), (2, 0), (2, 4), (3, 3), (4, 2)]),
                         [(1, 1), (2, 0), (2, 4), (3, 3), (4, 2)])


if __name__ == "__main__":
    unittest.main()
