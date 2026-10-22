import math
import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_measured(self) -> None:
        r = random.Random(1)
        got = []
        for n in (1024, 4096, 16384):
            c, s = [0], [0]
            out = ex.merge_sort([r.random() for _ in range(n)], c)
            ex.merge_sort(list(range(n)), s)
            self.assertEqual(out, sorted(out))
            got.append((c[0], s[0]))
        self.assertEqual(got, [(8925, 5120), (43938, 24576), (208705, 114688)])

    def test_trees(self) -> None:
        f = lambda s: s
        self.assertEqual([w for *_, w in ex.recursion_tree(16, 2, 2, f)], [16] * 5)
        self.assertEqual([w for *_, w in ex.recursion_tree(16, 4, 2, f)], [16, 32, 64, 128, 256])
        self.assertEqual([w for *_, w in ex.recursion_tree(16, 1, 2, f)], [16, 8, 4, 2, 1])
        self.assertEqual([ex.master(*t) for t in ((2, 2, 1), (4, 2, 1), (1, 2, 1), (3, 2, 1), (1, 2, 0))],
                         ["n^1 log n", "n^2.00", "n^1", "n^1.58", "n^0 log n"])
        self.assertEqual([ex.count_calls(16, a, 2) for a in (2, 4, 3, 1)], [31, 341, 121, 5])

    def test_general_theorem(self) -> None:
        self.assertEqual(ex.measured_ratios((256, 1024, 4096, 16384, 65536)),
                         [(256, 1721, 0.84, 1724), (1024, 8930, 0.872, 8945), (4096, 43950, 0.894, 43973),
                          (16384, 208706, 0.91, 208658), (65536, 965827, 0.921, 965706)])
        self.assertEqual(ex.master_general(2, 2, 1, 1), "n^1.00 log^2 n")
        self.assertIsNone(ex.master_general(2, 2, 1, -1))
        self.assertEqual(ex.master_general(3, 4, 1, 1), "n^1.00 log^1 n")
        self.assertEqual((ex.master_general(9, 3, 1), ex.master_general(8, 2, 2)), ("n^2.00", "n^3.00"))
        self.assertEqual(ex.master_general(1, 2, 0), "n^0.00 log^1 n")
        self.assertAlmostEqual(ex.regularity_ratio(3, 4, lambda n: n * math.log2(n), 1e6), 0.675, places=3)
        self.assertEqual(ex.regularity_ratio(2, 2, lambda n: n * n, 100), 0.5)
        self.assertEqual([w for *_, w in ex.recursion_tree(16, 2, 2, lambda s: s * math.log2(s))][:4], [64, 48, 32, 16])

    def test_substitution_and_uneven(self) -> None:
        self.assertEqual([ex.solve(n, [2, 2], lambda m: 1) for n in (1, 2, 4, 8, 16)], [1, 3, 7, 15, 31])
        self.assertEqual([ex.solve(n, [2], lambda m: m) for n in (1, 2, 4, 8, 16)], [1, 3, 7, 15, 31])
        self.assertTrue(all(ex.solve(n, [2], lambda m: m) <= 2 * n for n in range(1, 200)))
        self.assertEqual(ex.uneven_levels(27), [27, 27, 27, 27, 20, 15, 4, 3])
        self.assertEqual((ex.uneven_levels(1), ex.uneven_levels(2)), ([1], [2]))
        self.assertEqual([ex.akra_bazzi_p(t) for t in ([(1, 1 / 3), (1, 2 / 3)], [(2, .5)], [(3, .5)], [(1, .2), (1, .7)],
                                                     [(1, .1), (1, .9)])], [1.0, 1.0, 1.585, 0.84, 1.0])
        for k in (1, 2, 3, 4, 10):
            n, c = 2 ** k, [0]
            ex.merge_sort(ex.worst_order(n), c)
            self.assertEqual(c[0], n * k - n + 1)
        self.assertEqual(ex.worst_order(0), [])

    def test_every_case(self) -> None:
        c = [0]
        self.assertEqual((ex.merge_sort([], c), ex.merge_sort([5], c), c[0]), ([], [5], 0))
        self.assertEqual(ex.recursion_tree(1, 2, 2, lambda s: s), [(1, 1, 1)])
        self.assertEqual(ex.count_calls(1, 2, 2), 1)


if __name__ == "__main__":
    unittest.main()
