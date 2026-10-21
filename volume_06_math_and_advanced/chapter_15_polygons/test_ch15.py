import random
import unittest

import ch15_examples as ex


class TestChapter15(unittest.TestCase):
    def test_garden(self) -> None:
        self.assertEqual((ex.area(ex.GARDEN), ex.area(ex.GARDEN[::-1])), (36.0, -36.0))
        got = [ex.inside(p, ex.GARDEN) for p in ((2, 2), (4, 5), (8, 3), (4, 3), (6, 1), (9, 1), (2, 6))]
        self.assertEqual(got, ["inside", "outside", "edge", "edge", "inside", "outside", "outside"])

    def test_every_case(self) -> None:
        self.assertEqual((ex.area([]), ex.area([(0, 0), (1, 1)]), ex.area([(0, 0), (4, 0), (0, 3)])), (0.0, 0.0, 6.0))
        self.assertEqual((ex.inside((1, 1), [(0, 0), (4, 0), (0, 3)]), ex.area([(0, 0), (2, 0), (0, 2), (2, 2)])), ("inside", 0.0))
        self.assertEqual((ex.area([(0, 0), (5, 0), (5, 2), (0, 2)]), ex.inside((6, 4), ex.GARDEN)), (10.0, "inside"))
        self.assertEqual(sum(ex.inside((x, y), ex.GARDEN) == "inside" for x in range(9) for y in range(7)), 26)
        r = random.Random(15)
        square = [(0, 0), (10, 0), (10, 10), (0, 10)]
        for _ in range(300):
            p = (r.randint(-2, 12), r.randint(-2, 12))
            want = "edge" if (p[0] in (0, 10) and 0 <= p[1] <= 10) or (p[1] in (0, 10) and 0 <= p[0] <= 10) else \
                "inside" if 0 < p[0] < 10 and 0 < p[1] < 10 else "outside"
            self.assertEqual(ex.inside(p, square), want)


if __name__ == "__main__":
    unittest.main()
