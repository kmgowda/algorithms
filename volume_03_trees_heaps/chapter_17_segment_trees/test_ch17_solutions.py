import random
import unittest

import ch17_examples as ex
import ch17_solutions as sol


def brute(v, a, b):
    return max(sum(v[i:j + 1]) for i in range(a, b + 1) for j in range(i, b + 1))


class TestChapter17Solutions(unittest.TestCase):
    def test_largest_index(self) -> None:
        self.assertEqual([sol.largest_index(n) for n in range(0, 7)], [0, 1, 3, 5, 7, 9, 13])
        for n in range(1, 3000):
            self.assertLess(sol.largest_index(n), 4 * n)

    def test_best_stretch(self) -> None:
        self.assertIsNone(sol.BestStretchTree([]).best(0, 0))
        one = sol.BestStretchTree([-3])
        self.assertEqual(one.best(0, 0), -3)
        one.update(0, 4)
        self.assertEqual(one.best(0, 0), 4)
        g = sol.BestStretchTree([3, -4, 5, -1, 2, -6, 4, 1])
        self.assertEqual((g.best(0, 7), g.best(1, 4), g.best(5, 5), g.best(4, 2)), (6, 6, -6, None))
        g.update(5, 0)
        self.assertEqual(g.best(0, 7), 11)
        rng = random.Random(7)
        for _ in range(100):
            v = [rng.randint(-9, 9) for _ in range(rng.randint(1, 20))]
            t = sol.BestStretchTree(v)
            for _ in range(20):
                if rng.random() < 0.3:
                    i, x = rng.randrange(len(v)), rng.randint(-9, 9)
                    v[i] = x
                    t.update(i, x)
                a = rng.randrange(len(v))
                b = rng.randrange(a, len(v))
                self.assertEqual(t.best(a, b), brute(v, a, b))

    def test_forgetful_lazy_tree(self) -> None:
        bad, good = sol.ForgetfulLazyTree(ex.DAYS), ex.LazySegmentTree(ex.DAYS)
        bad.range_add(2, 5, 1)
        good.range_add(2, 5, 1)
        self.assertEqual((bad.query(0, 7), good.query(0, 7)), (31, 35))
        self.assertEqual((bad.query(0, 3), good.query(0, 3)), (9, 11))
        self.assertEqual(bad.query(2, 3), good.query(2, 3))
        one = sol.ForgetfulLazyTree([5])
        one.range_add(0, 0, 2)                           # a single box is always fully inside: no harm
        self.assertEqual(one.query(0, 0), 7)


if __name__ == "__main__":
    unittest.main()
