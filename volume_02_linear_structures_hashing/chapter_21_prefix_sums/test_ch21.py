import random
import unittest

import ch21_examples as ex


class TestChapter37(unittest.TestCase):
    def test_every_case(self) -> None:
        p = ex.prefix_sums(ex.VISITS)
        self.assertEqual(ex.prefix_sums([]), [0])
        self.assertEqual([ex.range_sum(p, a, b) for a, b in ((0, 9), (4, 4), (0, 0), (9, 9))], [39, 5, 3, 3])
        self.assertEqual(ex.chairs_in_use([], 5), [0] * 5)
        self.assertEqual(ex.chairs_in_use([(0, 4, 2)], 5), [2] * 5)
        self.assertEqual(ex.chairs_in_use([(2, 2, 1)], 5), [0, 0, 1, 0, 0])
        self.assertEqual(ex.chairs_in_use([(0, 1, 1), (1, 2, 1)], 3), [1, 2, 1])
        self.assertEqual([ex.count_stretches_with_sum(a, k) for a, k in (([], 0), ([0, 0], 0), ([1, -1, 1], 0),
                                                                       (ex.VISITS, 100), (ex.VISITS, 10))], [0, 3, 2, 0, 1])
        gp = ex.grid_prefix([[1, 0, 2], [0, 3, 1], [2, 1, 0]])
        self.assertEqual((ex.block_sum(gp, 0, 0, 2, 2), ex.block_sum(gp, 1, 1, 1, 1), ex.block_sum(gp, 0, 2, 2, 2)), (10, 3, 3))

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-5, 9) for _ in range(rng.randint(1, 12))]
            p = ex.prefix_sums(v)
            a = rng.randrange(len(v)); b = rng.randrange(a, len(v))
            self.assertEqual(ex.range_sum(p, a, b), sum(v[a:b + 1]))
            k = rng.randint(-5, 15)
            brute = sum(1 for i in range(len(v)) for j in range(i + 1, len(v) + 1) if sum(v[i:j]) == k)
            self.assertEqual(ex.count_stretches_with_sum(v, k), brute)
            hours = rng.randint(1, 12)
            bookings = []
            for _ in range(rng.randint(0, 6)):
                s = rng.randrange(hours); e = rng.randrange(s, hours)
                bookings.append((s, e, rng.randint(1, 4)))
            direct = [sum(c for s, e, c in bookings if s <= h <= e) for h in range(hours)]
            self.assertEqual(ex.chairs_in_use(bookings, hours), direct)
            g = [[rng.randint(0, 5) for _ in range(4)] for _ in range(3)]
            gp = ex.grid_prefix(g)
            self.assertEqual(ex.block_sum(gp, 1, 1, 2, 3), sum(g[r][c] for r in (1, 2) for c in (1, 2, 3)))

    def test_examples(self) -> None:
        p = ex.prefix_sums(ex.VISITS)
        self.assertEqual((ex.range_sum(p, 3, 7), ex.range_sum(p, 0, 4), ex.range_sum(p, 6, 9)), (23, 14, 16))
        self.assertEqual(ex.chairs_in_use([(1, 4, 2), (3, 6, 1), (0, 2, 3), (5, 8, 4)], 10),
                         [3, 5, 5, 3, 3, 5, 5, 4, 4, 0])
        self.assertEqual(ex.count_stretches_with_sum(ex.VISITS, 10), 1)
        gp = ex.grid_prefix([[1, 0, 2], [0, 3, 1], [2, 1, 0]])
        self.assertEqual((ex.block_sum(gp, 1, 1, 2, 2), ex.block_sum(gp, 0, 0, 1, 1)), (5, 4))


class TestGridBuildAndCounting(unittest.TestCase):
    def test_grid_build(self) -> None:
        self.assertEqual(ex.grid_prefix([[1, 0, 2], [0, 3, 1], [2, 1, 0]]),
                         [[0, 0, 0, 0], [0, 1, 1, 3], [0, 1, 4, 7], [0, 3, 7, 10]])
        self.assertEqual((ex.grid_prefix([]), ex.grid_prefix([[]]), ex.grid_prefix([[5]])), ([[0]], [[0], [0]], [[0, 0], [0, 5]]))

    def test_counting(self) -> None:
        self.assertEqual(ex.count_stretches_with_sum([2, 3, -1, 1, 5], 5), 4)
        self.assertEqual(ex.count_stretches_with_sum([1, -1, 1, -1], 0), 4)


if __name__ == "__main__":
    unittest.main()
