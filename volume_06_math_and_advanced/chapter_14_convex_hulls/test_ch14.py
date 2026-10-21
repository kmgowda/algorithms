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
        r = random.Random(1)
        for _ in range(200):
            pts = [(r.randint(0, 9), r.randint(0, 9)) for _ in range(r.randint(3, 15))]
            self.assertTrue(ex.encloses(ex.convex_hull(pts), pts))


if __name__ == "__main__":
    unittest.main()
