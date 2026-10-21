import itertools
import random
import unittest

import ch23_examples as ex


class TestChapter23(unittest.TestCase):
    def test_examples(self) -> None:
        c = ex.cover_by_matching(ex.ROADS)
        self.assertEqual((len(c), len(ex.smallest_cover(ex.TOWN, ex.ROADS))), (8, 4))
        boxes = [7, 6, 5, 4, 4, 3, 2, 2, 2, 1]
        self.assertEqual((ex.first_fit_decreasing(boxes, 10), ex.fewest_bins(boxes, 10)), ([[7, 3], [6, 4], [5, 4, 1], [2, 2, 2]], 4))

    def test_every_case(self) -> None:
        self.assertEqual((ex.cover_by_matching([]), ex.first_fit_decreasing([], 10), ex.first_fit_decreasing([10, 10], 10), ex.cover_by_matching([("a", "b")])),
                         ([], [], [[10], [10]], ["a", "b"]))
        with self.assertRaises(ValueError):
            ex.first_fit_decreasing([11], 10)
        roads = [("Market", "Station")] + [x for x in ex.ROADS if x != ("Market", "Station")]
        self.assertEqual((len(ex.cover_by_matching(roads)), ex.first_fit_decreasing([6, 5, 5, 4], 10)), (8, [[6, 4], [5, 5]]))
        self.assertEqual(ex.cover_by_matching([("a", "b"), ("c", "d")]), ["a", "b", "c", "d"])
        r = random.Random(23)
        for _ in range(150):
            vs = list(range(7))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.35]
            c = ex.cover_by_matching(es)
            self.assertTrue(all(a in c or b in c for a, b in es))
            self.assertLessEqual(len(c), 2 * len(ex.smallest_cover(vs, es)))
            sizes = [r.randint(1, 10) for _ in range(r.randint(1, 6))]
            self.assertLessEqual(len(ex.first_fit_decreasing(sizes, 10)), 11 * ex.fewest_bins(sizes, 10) // 9 + 1)


if __name__ == "__main__":
    unittest.main()
