import random
import unittest

import ch15_examples as ex


class TestChapter12(unittest.TestCase):
    def test_sorts_and_stable(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 15) for _ in range(rng.randint(0, 40))]
            b = list(a)
            ex.timsort(b)
            self.assertEqual(b, sorted(a))
        recs = [(rng.randint(0, 4), i) for i in range(60)]

        class K:
            def __init__(self, r): self.r = r
            def __lt__(self, o): return self.r[0] < o.r[0]
            def __le__(self, o): return self.r[0] <= o.r[0]
            def __ge__(self, o): return self.r[0] >= o.r[0]
        b = [K(r) for r in recs]
        ex.timsort(b)
        self.assertEqual([k.r for k in b], sorted(recs, key=lambda r: r[0]))

    def test_every_case(self) -> None:
        p = list(ex.PILE)
        rows = [(p, 5, 27, 21), (sorted(p), 1, 8, 13), (sorted(p, reverse=True), 1, 8, 16), ([47] * 9, 1, 8, 13),
                ([12, 31, 58, 70, 91, 25, 47, 63, 84], 2, 16, 18), ([47], 1, 0, 0), ([], 0, 0, 0)]
        for a, runs, tim, mer in rows:
            self.assertEqual(len(ex.find_runs(list(a))), runs)
            b, c = list(a), {"comparisons": 0}
            ex.timsort(b, c)
            self.assertEqual((b, c["comparisons"], ex.merge_sort_comparisons(a)), (sorted(a), tim, mer))

    def test_examples(self) -> None:
        a, log = list(ex.PILE), []
        ex.timsort(a, log=log)
        self.assertEqual(log[0], ("runs", [[25, 58], [12, 91], [47, 70], [31, 84], [63]]))
        a = [3, 7, 9, 6, 4, 2, 5, 8]
        self.assertEqual([a[s:e] for s, e in ex.find_runs(a)], [[3, 7, 9], [2, 4, 6], [5, 8]])

    def test_min_run(self) -> None:
        self.assertEqual([ex.min_run(n) for n in (0, 1, 9, 63, 64, 65, 100, 1000, 2112, 1_000_000)],
                         [0, 1, 9, 63, 32, 33, 50, 63, 33, 62])
        for n in range(64, 5000):
            m = ex.min_run(n)
            self.assertTrue(32 <= m <= 64)
            k = n.bit_length() - 6                           # n / m is a power of two, or a little below one
            self.assertTrue(2 ** (k - 1) < n / m <= 2 ** k)

    def test_collapse_rule(self) -> None:
        log = []
        self.assertEqual(ex.collapse_rule([50, 30, 25], log), [105])
        self.assertEqual(log, [(30, 25), (50, 55)])
        self.assertEqual(ex.collapse_rule([105, 20]), [105, 20])
        self.assertEqual(ex.collapse_rule([]), [])
        self.assertEqual(ex.collapse_rule([7]), [7])
        rng = random.Random(3)
        for _ in range(300):
            st = []
            for _ in range(rng.randint(1, 30)):
                st = ex.collapse_rule(st + [rng.randint(1, 100)])
                for i in range(len(st) - 1):
                    self.assertGreater(st[i], st[i + 1])
                for i in range(len(st) - 2):
                    self.assertGreater(st[i], st[i + 1] + st[i + 2])

    def test_merge_policies(self) -> None:
        runs = [1000, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(ex.timsort_merges(runs), [(1, 1), (1, 1), (2, 2), (1, 1), (2, 1), (4, 3), (1000, 7)])
        self.assertEqual(ex.merge_cost(ex.timsort_merges(runs)), 1027)
        self.assertEqual(ex.merge_cost(ex.powersort_merges(runs)), 1027)
        self.assertEqual(ex.merge_cost([(1000 + i, 1) for i in range(7)]), 7028)
        self.assertEqual(ex.timsort_merges([]), [])
        self.assertEqual(ex.powersort_merges([]), [])
        self.assertEqual(ex.powersort_merges([5]), [])
        self.assertEqual(ex.powersort_merges([3, 4]), [(3, 4)])
        rng = random.Random(4)
        for _ in range(200):
            rs = [rng.randint(1, 50) for _ in range(rng.randint(1, 20))]
            for policy in (ex.timsort_merges, ex.powersort_merges):
                m = policy(rs)
                self.assertEqual(len(m), len(rs) - 1)
                self.assertEqual(m[-1][0] + m[-1][1] if m else rs[0], sum(rs))


if __name__ == "__main__":
    unittest.main()
