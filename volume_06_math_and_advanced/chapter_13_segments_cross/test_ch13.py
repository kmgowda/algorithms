import random
import unittest

import ch13_examples as ex


class TestChapter13(unittest.TestCase):
    def test_paths(self) -> None:
        self.assertEqual(ex.crossing_pairs(ex.PATHS), [("A", "B"), ("A", "D")])

    def test_every_case(self) -> None:
        got = [ex.segments_cross(*s) for s in (((0, 0), (4, 0), (2, 0), (6, 0)), ((0, 0), (2, 0), (3, 0), (5, 0)),
                                                ((0, 0), (2, 2), (2, 2), (4, 0)), ((0, 0), (2, 2), (3, 3), (5, 5)), ((1, 1), (1, 1), (0, 0), (2, 2)))]
        self.assertEqual(got, [True, False, True, False, True])
        self.assertEqual((ex.segments_cross((1, 1), (7, 3), (0, 4), (6, 0)), ex.segments_cross((1, 1), (7, 3), (0, 0), (6, 4)),
                          ex.segments_cross((0, 4), (6, 0), (2, 0), (4, 0))), (True, True, False))
        r = random.Random(13)
        for _ in range(300):
            s = [(r.randint(0, 4), r.randint(0, 4)) for _ in range(4)]
            self.assertEqual(ex.segments_cross(*s), ex.segments_cross(s[2], s[3], s[0], s[1]))


class TestDepth(unittest.TestCase):
    def test_intersection_point(self) -> None:
        from fractions import Fraction as F
        self.assertEqual(ex.intersection_point(*ex.PATHS["A"], *ex.PATHS["B"]), (3, 2))
        self.assertEqual(ex.intersection_point((1, 1), (7, 3), *ex.PATHS["B"]), (F(10, 3), F(16, 9)))
        self.assertIsNone(ex.intersection_point((0, 0), (4, 0), (2, 0), (6, 0)))      # overlapping: no single point
        self.assertIsNone(ex.intersection_point(*ex.PATHS["C"], *ex.PATHS["E"]))

    def test_chapter_numbers(self) -> None:
        from fractions import Fraction as F
        self.assertEqual(ex.any_crossing([ex.PATHS["A"], ex.PATHS["B"], ex.PATHS["E"]]), ((0, 1), 1))
        self.assertEqual(ex.intersection_point((0, 0), (4, 4), (0, 3), (3, 0)), (F(3, 2), F(3, 2)))
        self.assertTrue(ex.segments_cross((0, 0), (4, 0), (2, 0), (2, 3)))

    def test_shamos_hoey(self) -> None:
        nonvert = [ex.PATHS[k] for k in ("A", "B", "C", "D", "E")]
        self.assertEqual(ex.any_crossing(nonvert), ((0, 1), 1))
        self.assertEqual(ex.any_crossing([]), (None, 0))
        self.assertEqual(ex.any_crossing([ex.PATHS["C"]]), (None, 0))
        with self.assertRaises(ValueError):
            ex.any_crossing([((0, 0), (0, 5))])
        import random
        r = random.Random(14)
        for _ in range(400):
            n = r.randint(0, 25)
            segs = []
            while len(segs) < n:
                a = (r.randint(0, 10 ** 6), r.randint(0, 10 ** 6))
                b = (r.randint(0, 10 ** 6), r.randint(0, 10 ** 6))
                if a[0] != b[0]:
                    segs.append((a, b))
            found, _ = ex.any_crossing(segs)
            self.assertEqual(found is not None, ex.any_crossing_brute(segs))
            if found:
                self.assertTrue(ex.segments_cross(*segs[found[0]], *segs[found[1]]))


if __name__ == "__main__":
    unittest.main()
