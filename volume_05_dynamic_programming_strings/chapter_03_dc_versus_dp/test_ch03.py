import math
import unittest
from collections import Counter

import ch03_examples as ex


class TestChapter3(unittest.TestCase):
    def test_compare(self) -> None:
        got = []
        for n in (8, 16, 1024):
            s = Counter()
            ex.merge_sort_ranges(0, n, s)
            got.append(ex.summary(s))
        self.assertEqual(got, [(15, 15), (31, 31), (2047, 2047)])
        got = []
        for n, k in ((6, 3), (10, 5), (20, 10)):
            s = Counter()
            got.append((ex.choose(n, k, s), ex.summary(s), ex.choose_table(n, k)))
        self.assertEqual(got, [(20, (39, 15), (20, 28)), (252, (503, 35), (252, 66)), (184756, (369511, 120), (184756, 231))])
        s = Counter()
        ex.choose(6, 3, s)
        self.assertEqual(s[(2, 1)], 6)

    def test_every_case(self) -> None:
        s = Counter()
        ex.merge_sort_ranges(0, 1, s)
        self.assertEqual(ex.summary(s), (1, 1))
        self.assertEqual((ex.choose(5, 0, Counter()), ex.choose(5, 5, Counter()), ex.choose_table(0, 0), ex.choose_table(5, 0)),
                         (1, 1, (1, 1), (1, 21)))
        s = Counter()
        ex.choose(4, 2, s)
        self.assertEqual(ex.summary(s), (11, 8))
        for n in range(12):
            for k in range(n + 1):
                self.assertEqual(ex.choose_table(n, k)[0], math.comb(n, k))


    def test_sub_problem_graph(self) -> None:
        edges, order = ex.sub_problem_graph(4, 2)
        self.assertEqual((len(order), len(edges)), (8, 8))
        pos = {v: i for i, v in enumerate(order)}
        self.assertTrue(all(pos[b] < pos[a] for a, b in edges))
        self.assertEqual(ex.sub_problem_graph(3, 0), ([], [(3, 0)]))
        self.assertEqual(len(ex.sub_problem_graph(20, 10)[1]), 120)


if __name__ == "__main__":
    unittest.main()
