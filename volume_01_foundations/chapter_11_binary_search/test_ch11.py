import bisect
import random
import unittest

import ch11_examples as ex


class TestChapter11(unittest.TestCase):
    def test_every_case(self) -> None:
        rows = [(58, 4, [4]), (12, 0, [4, 1, 0]), (91, 8, [4, 6, 7, 8]), (50, -1, [4, 1, 2, 3]), (5, -1, [4, 1, 0]),
                (95, -1, [4, 6, 7, 8])]
        for target, pos, looked in rows:
            r = ex.binary_search(ex.SHELF, target)
            self.assertEqual((r[0], r[2]), (pos, looked))
        self.assertEqual([ex.binary_search(ex.SHELF, t)[1] for t in (50, 5, 95)], [4, 0, 9])
        self.assertEqual(ex.binary_search([], 5), (-1, 0, []))
        self.assertEqual((ex.binary_search([47], 47)[0], ex.binary_search([47], 12)[0]), (0, -1))
        dup = [12, 25, 47, 47, 47, 63, 70, 84, 91]
        self.assertEqual((ex.binary_search(dup, 47)[0], ex.lower_bound(dup, 47)), (4, 2))
        self.assertEqual(ex.binary_search([47, 12, 91, 25], 25)[0], -1)     # unsorted: a wrong answer

    def test_against_bisect(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            xs = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 15)))
            t = rng.randint(-2, 32)
            pos, low, looked = ex.binary_search(xs, t)
            if t in xs:
                self.assertEqual(xs[pos], t)
            else:
                self.assertEqual(pos, -1)
                self.assertEqual(low, bisect.bisect_left(xs, t))
            self.assertLessEqual(len(looked), ex.worst_looks(len(xs)) if xs else 0)
            self.assertEqual(ex.lower_bound(xs, t), bisect.bisect_left(xs, t))

    def test_examples(self) -> None:
        self.assertEqual(ex.binary_search(ex.SHELF, 63)[2], [4, 6, 5])
        self.assertEqual(ex.binary_search(ex.SHELF, 50), (-1, 4, [4, 1, 2, 3]))
        self.assertEqual(ex.binary_search(ex.SHELF, 25)[2], [4, 1])
        self.assertEqual(ex.binary_search(ex.SHELF, 95)[1], 9)
        self.assertEqual(ex.lower_bound([12, 25, 47, 47, 47, 63], 47), 2)
        self.assertEqual([ex.worst_looks(n) for n in (9, 100, 4000, 10 ** 6, 10 ** 9)], [4, 7, 12, 20, 30])
        self.assertEqual(ex.binary_search([47, 12, 91, 25], 25)[0], -1)

    def test_upper_bound_and_copies(self) -> None:
        dup = [12, 25, 47, 47, 47, 63, 70, 84, 91]
        self.assertEqual((ex.lower_bound(dup, 47), ex.upper_bound(dup, 47), ex.count_copies(dup, 47)), (2, 5, 3))
        self.assertEqual((ex.upper_bound([], 5), ex.count_copies([], 5)), (0, 0))
        self.assertEqual((ex.upper_bound([47], 47), ex.count_copies([47], 47), ex.count_copies([47], 12)), (1, 1, 0))
        self.assertEqual((ex.upper_bound([7] * 6, 7), ex.lower_bound([7] * 6, 7), ex.count_copies([7] * 6, 7)),
                         (6, 0, 6))
        self.assertEqual((ex.count_copies(dup, 50), ex.lower_bound(dup, 50), ex.upper_bound(dup, 50)), (0, 5, 5))
        self.assertEqual((ex.upper_bound(dup, 5), ex.upper_bound(dup, 95)), (0, 9))
        rng = random.Random(2)
        for _ in range(500):
            xs = sorted(rng.randint(0, 10) for _ in range(rng.randint(0, 15)))
            t = rng.randint(-1, 11)
            self.assertEqual(ex.upper_bound(xs, t), bisect.bisect_right(xs, t))
            self.assertEqual(ex.count_copies(xs, t), xs.count(t))


if __name__ == "__main__":
    unittest.main()
