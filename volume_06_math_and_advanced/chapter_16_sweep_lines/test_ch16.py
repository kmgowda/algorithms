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


if __name__ == "__main__":
    unittest.main()
