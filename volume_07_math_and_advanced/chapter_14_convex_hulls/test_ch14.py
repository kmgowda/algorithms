import random
import unittest

import ch14_examples as ex


class TestChapter14(unittest.TestCase):
    def test_boxes(self) -> None:
        h = ex.convex_hull(ex.BOXES)
        self.assertEqual((h, round(ex.perimeter(h), 2)), ([(2, 3), (5, 1), (35, 8), (40, 50), (12, 30)], 139.91))
        r = random.Random(14)
        pts = [(r.randint(0, 1000), r.randint(0, 1000)) for _ in range(10000)]
        self.assertEqual(len(ex.convex_hull(pts)), 16)

    def test_every_case(self) -> None:
        self.assertEqual([ex.convex_hull(p) for p in ([], [(1, 1)], [(1, 1), (1, 1)], [(0, 0), (1, 1), (2, 2)])], [[], [(1, 1)], [(1, 1)], [(0, 0), (2, 2)]])
        self.assertEqual(ex.convex_hull([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (2, 0)]), [(0, 0), (4, 0), (4, 4), (0, 4)])
        self.assertEqual(ex.perimeter([(1, 1)]), 0.0)
        import itertools, math
        h = ex.convex_hull(ex.BOXES)
        self.assertEqual(max((math.dist(a, b), a, b) for a, b in itertools.combinations(h, 2))[1:], ((2, 3), (40, 50)))
        r = random.Random(1)
        for _ in range(200):
            pts = [(r.randint(0, 9), r.randint(0, 9)) for _ in range(r.randint(3, 15))]
            self.assertTrue(ex.encloses(ex.convex_hull(pts), pts))


class TestDepth(unittest.TestCase):
    def test_three_methods_agree(self) -> None:
        log = []
        self.assertEqual(ex.graham_scan(ex.BOXES, log), [(5, 1), (35, 8), (40, 50), (12, 30), (2, 3)])
        self.assertEqual([e for e in log if e[0] == "pop"], [("pop", (12, 10), (40, 50)), ("pop", (20, 25), (12, 30)), ("pop", (3, 4), (2, 3))])
        self.assertEqual(ex.jarvis_march(ex.BOXES), ([(2, 3), (5, 1), (35, 8), (40, 50), (12, 30)], 35))
        import random
        r = random.Random(15)
        for trial in range(400):
            n = r.randint(0, 40)
            k = r.choice([3, 10, 1000])
            pts = [(r.randint(0, k), r.randint(0, k)) for _ in range(n)]
            if trial % 7 == 0:
                pts = [(i, 2 * i + 1) for i in range(r.randint(0, 6))]           # all in a line
            a = ex.rotate_hull(ex.convex_hull(pts))
            self.assertEqual(ex.rotate_hull(ex.graham_scan(pts)), a)
            self.assertEqual(ex.rotate_hull(ex.jarvis_march(pts)[0]), a)

    def test_calipers(self) -> None:
        h = ex.convex_hull(ex.BOXES)
        d, p, q, steps = ex.rotating_calipers(h)
        self.assertEqual((round(d, 2), {p, q}, steps), (60.44, {(2, 3), (40, 50)}, 16))
        self.assertEqual((ex.rotating_calipers([(1, 1)])[0], ex.rotating_calipers([(0, 0), (3, 4)])[0]), (0.0, 5.0))
        import random
        r = random.Random(16)
        for _ in range(300):
            pts = [(r.randint(0, 100), r.randint(0, 100)) for _ in range(r.randint(1, 60))]
            hull = ex.convex_hull(pts)
            self.assertAlmostEqual(ex.rotating_calipers(hull)[0], ex.diameter_brute(hull)[0] if len(hull) > 1 else 0.0)


    def test_delaunay(self) -> None:
        import random
        tris = ex.delaunay_brute(ex.BRANCHES)
        self.assertEqual(len(tris), 5)
        self.assertEqual(ex.nearest_branch(ex.BRANCHES, (5, 5)), (4, 4))
        r = random.Random(14)
        for _ in range(30):
            pts = list({(r.randint(0, 40), r.randint(0, 40)) for _ in range(r.randint(3, 9))})
            hull = ex.convex_hull(pts)
            if len(hull) < 3 or len(pts) < 3:
                continue
            tris = ex.delaunay_brute(pts)
            if len(tris) == 2 * len(pts) - 2 - len(hull):    # general position: Euler's formula holds exactly
                for a, b, c in tris:
                    if ex.cross(a, b, c) < 0:
                        b, c = c, b
                    self.assertTrue(all(ex.in_circle(a, b, c, d) <= 0 for d in pts if d not in (a, b, c)))


if __name__ == "__main__":
    unittest.main()
