import math
import random
import unittest

import ch22_examples as ex


class TestChapter20(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.inversions_brute(ex.RANKS), ex.sort_count(ex.RANKS)[1]), (9, 9))
        d, pair = ex.closest_pair(ex.BOXES)
        self.assertEqual((round(d, 3), pair), (1.414, ((2, 3), (3, 4))))

    def test_every_case(self) -> None:
        self.assertEqual([ex.sort_count(a)[1] for a in ([], [1, 2, 3], [3, 2, 1], [2, 2, 1], list(range(8, 0, -1)))], [0, 0, 3, 2, 28])
        self.assertEqual(ex.closest_pair([(0, 0), (3, 4)])[0], 5.0)
        self.assertEqual([ex.sort_count(a)[1] for a in ([1, 2, 3, 4, 5, 6, 8, 7], [4, 3, 2, 1], [2, 7, 3, 5])], [1, 6, 2])
        self.assertEqual(ex.closest_pair([(1, 1), (1, 1), (5, 5)])[0], 0.0)
        r = random.Random(1)
        for _ in range(300):
            p = [(r.randint(0, 50), r.randint(0, 50)) for _ in range(r.randint(2, 25))]
            self.assertTrue(math.isclose(ex.closest_pair(p)[0], ex.closest_brute(p)[0]))
            a = [r.randint(0, 9) for _ in range(r.randint(0, 20))]
            self.assertEqual(ex.sort_count(a)[1], ex.inversions_brute(a))
            self.assertTrue(math.isclose(ex.closest_pair_resorting(p), ex.closest_brute(p)[0]))

    def test_presorted_closest_pair(self) -> None:
        self.assertEqual(ex.closest_pair([]), (math.inf, None))
        self.assertEqual(ex.closest_pair([(4, 4)]), (math.inf, None))
        self.assertEqual(ex.closest_pair([(1, 1), (1, 1)]), (0.0, ((1, 1), (1, 1))))
        self.assertEqual(ex.closest_pair([(0, y) for y in (0, 5, 7, 20)])[0], 2.0)     # every x equal
        r = random.Random(5)
        for n in (1000, 4000):
            pts = [(r.random(), r.random()) for _ in range(n)]
            c = [0]
            d = ex.closest_pair(pts, c)[0]
            self.assertTrue(math.isclose(d, ex.closest_pair_resorting(pts)))
            self.assertLess(c[0], 2 * n)                                              # about 1.15 n distances
        self.assertLessEqual(ex.strip_candidates([(r.randint(0, 9), r.randint(0, 9)) for _ in range(60)], 5, 1.0), 7)
        self.assertEqual(ex.jumps([1, 3, 4, 8], [2, 5, 6, 7]), [(2, 3), (5, 1), (6, 1), (7, 1)])
        self.assertEqual(ex.jumps([], [1]), [])
        self.assertEqual(ex.sort_count([5, 2, 6, 1])[1], 4)
        self.assertEqual(round(ex.kendall_tau(ex.RANKS), 2), 0.36)
        self.assertEqual((ex.kendall_tau([1, 2, 3]), ex.kendall_tau([3, 2, 1])), (1.0, -1.0))
        for _ in range(200):
            a = [r.randint(0, 30) for _ in range(r.randint(0, 15))]
            self.assertEqual(ex.significant_count(a),
                             sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > 2 * a[j]))


if __name__ == "__main__":
    unittest.main()
