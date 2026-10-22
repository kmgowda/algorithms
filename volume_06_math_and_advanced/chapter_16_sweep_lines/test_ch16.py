import random
import unittest

import ch16_examples as ex


class TestChapter16(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.max_overlap(ex.BOOKINGS), ex.union_area(ex.TABLES)), ((3, 16), 17))
        r = random.Random(16)
        pts = [(r.randint(0, 10 ** 6), r.randint(0, 10 ** 6)) for _ in range(3000)]
        self.assertEqual(ex.closest_by_sweep(pts), (102149, 4448))

    def test_every_case(self) -> None:
        self.assertEqual((ex.max_overlap([])[0], ex.max_overlap([(9, 10), (10, 11)])[0]), (0, 1))
        self.assertEqual([ex.union_area(x) for x in ([], [(0, 0, 2, 2), (0, 0, 2, 2)], [(0, 0, 1, 1), (3, 3, 4, 4)])], [0, 4, 2])
        self.assertEqual(ex.closest_by_sweep([(0, 0), (0, 0)])[0], 0)
        r = random.Random(1)
        for _ in range(200):
            rects = []
            for _ in range(r.randint(1, 5)):
                x, y = r.randint(0, 8), r.randint(0, 8)
                rects.append((x, y, x + r.randint(1, 4), y + r.randint(1, 4)))
            self.assertEqual(ex.union_area(rects), ex.union_area_by_cells(rects))
            pts = [(r.randint(0, 20), r.randint(0, 20)) for _ in range(r.randint(2, 15))]
            brute = min((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for i, a in enumerate(pts) for b in pts[i + 1:])
            self.assertEqual(ex.closest_by_sweep(pts)[0], brute)


class TestDepth(unittest.TestCase):
    def test_closest_pair_sweep(self) -> None:
        line_pts = [(0, 3 * i) for i in range(2000)]
        self.assertEqual((ex.closest_by_sweep(line_pts), ex.closest_pair_sweep(line_pts)), ((9, 1999000), (9, 1999)))
        self.assertEqual((ex.closest_pair_sweep([]), ex.closest_pair_sweep([(1, 1)])), ((float("inf"), 0), (float("inf"), 0)))
        self.assertEqual(ex.closest_pair_sweep([(2, 2), (2, 2)])[0], 0)
        import random
        r = random.Random(18)
        for _ in range(300):
            k = r.choice([5, 50, 10 ** 6])
            pts = [(r.randint(0, k), r.randint(0, k)) for _ in range(r.randint(2, 60))]
            self.assertEqual(ex.closest_pair_sweep(pts)[0], ex.closest_brute(pts))

    def test_strips_and_skyline(self) -> None:
        self.assertEqual(ex.strip_heights(ex.TABLES), [(0, 2, 2), (2, 4, 3), (4, 5, 2), (5, 6, 3), (6, 7, 2)])
        self.assertEqual(ex.skyline([(1, 5, 3), (2, 4, 6), (3, 9, 2), (7, 8, 4)]), [(1, 3), (2, 6), (4, 3), (5, 2), (7, 4), (8, 2), (9, 0)])
        self.assertEqual((ex.skyline([]), ex.skyline([(0, 2, 5)])), ([], [(0, 5), (2, 0)]))
        self.assertEqual(ex.skyline([(0, 2, 5), (2, 4, 5)]), [(0, 5), (4, 0)])


if __name__ == "__main__":
    unittest.main()
