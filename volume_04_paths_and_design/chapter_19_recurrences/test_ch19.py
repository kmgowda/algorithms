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

    def test_every_case(self) -> None:
        c = [0]
        self.assertEqual((ex.merge_sort([], c), ex.merge_sort([5], c), c[0]), ([], [5], 0))
        self.assertEqual(ex.recursion_tree(1, 2, 2, lambda s: s), [(1, 1, 1)])
        self.assertEqual(ex.count_calls(1, 2, 2), 1)


if __name__ == "__main__":
    unittest.main()
