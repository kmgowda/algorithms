import bisect
import random
import unittest

import ch11_examples as ex


class TestChapter11(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
