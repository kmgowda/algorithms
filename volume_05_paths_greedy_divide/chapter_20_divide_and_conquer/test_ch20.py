import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_festival(self) -> None:
        log = []
        self.assertEqual((ex.total(ex.VISITORS, 0, log), len(log)), (111, 15))
        a, b = [0], [0]
        self.assertEqual((ex.min_max(ex.VISITORS, a), a[0], ex.min_max_simple(ex.VISITORS, b), b[0]), ((3, 26), 10, (3, 26), 14))
        self.assertEqual(ex.best_stretch([5, -9, 6, -2, 3, -1, 4, -8]), (10, 2, 6))

    def test_every_case(self) -> None:
        self.assertEqual((ex.total([]), ex.total([4])), (0, 4))
        counts = []
        for n in (1, 2, 3, 16, 1000):
            a, b = [0], [0]
            ex.min_max(list(range(n)), a)
            ex.min_max_simple(list(range(n)), b)
            counts.append((a[0], b[0]))
        self.assertEqual(counts, [(0, 0), (1, 2), (3, 4), (22, 30), (1510, 1998)])
        self.assertEqual((ex.best_stretch([-3, -1, -2]), ex.best_stretch([7])), ((-1, 1, 1), (7, 0, 0)))
        self.assertEqual(ex.best_stretch([2, 1, -8, -1, -1, -1, -1, -1]), (3, 0, 1))
        rng = random.Random(3)
        for _ in range(200):
            v = [rng.randint(-9, 9) for _ in range(rng.randint(1, 12))]
            self.assertEqual(ex.best_stretch(v)[0], max(sum(v[i:j + 1]) for i in range(len(v)) for j in range(i, len(v))))
            self.assertEqual(ex.stretch_summary(v)[1], ex.best_stretch(v)[0])

    def test_crossing(self) -> None:
        changes = [5, -9, 6, -2, 3, -1, 4, -8]
        self.assertEqual(ex.crossing(changes, 0, 4, 8), 10)
        self.assertEqual((ex.crossing(changes, 0, 2, 4), ex.crossing(changes, 4, 6, 8)), (2, 6))
        self.assertEqual(ex.crossing([4, -1, -3, 2, 5, -6, 1, 3], 0, 4, 8), 7)
        self.assertEqual(ex.crossing([1, 2], 0, 1, 2), 3)
        self.assertEqual(ex.stretch_summary([7]), (7, 7, 7, 7))
        self.assertEqual(ex.stretch_summary(changes)[1], 10)


if __name__ == "__main__":
    unittest.main()
