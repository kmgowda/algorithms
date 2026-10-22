import itertools
import random
import unittest

import ch28_examples as ex


class TestChapter25(unittest.TestCase):
    def test_examples(self) -> None:
        c = [0]
        self.assertEqual((ex.cover_branching(ex.ROADS, 4, c), c[0], ex.cover_brute(ex.TOWN, ex.ROADS, 4)[1]), (["School", "Park", "Station", "Museum"], 31, 133))
        c = [0]
        self.assertEqual((ex.cover_branching(ex.ROADS, 3, c), c[0]), (None, 15))
        r = random.Random(25)
        vals = [r.randint(1, 10 ** 6) for _ in range(24)]
        self.assertEqual((ex.subset_sum_mitm(vals, sum(vals[::3])), ex.subset_sum_mitm(vals, 1)), ((True, 8192), (False, 8192)))

    def test_every_case(self) -> None:
        self.assertEqual((ex.cover_branching([], 0, [0]), ex.cover_branching([("a", "b")], 0, [0])), ([], None))
        self.assertEqual((ex.subset_sum_mitm([], 0), ex.subset_sum_mitm([], 3), ex.subset_sum_mitm([5], 5)), ((True, 2), (False, 2), (True, 3)))
        r = random.Random(1)
        for _ in range(100):
            vs = list(range(7))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.35]
            k = r.randint(0, 5)
            self.assertEqual(ex.cover_branching(es, k, [0]) is None, ex.cover_brute(vs, es, k)[0] is None)
            vals = [r.randint(1, 20) for _ in range(r.randint(0, 8))]
            t = r.randint(0, 60)
            want = any(sum(c) == t for n in range(len(vals) + 1) for c in itertools.combinations(vals, n))
            self.assertEqual(ex.subset_sum_mitm(vals, t)[0], want)


class TestDepth(unittest.TestCase):
    def test_kernel_and_branching(self) -> None:
        self.assertEqual(ex.subset_sum_mitm_trace([12, 7, 15, 9], 31), ([0, 7, 12, 19], [0, 9, 15, 24], (7, 24)))
        star = [("hub", f"leaf{i}") for i in range(30)] + [("a", "b"), ("b", "c")]
        self.assertEqual(ex.buss_kernel(star, 3), ([("a", "b"), ("b", "c")], ["hub"], 2))
        self.assertEqual(ex.buss_kernel(ex.ROADS, 2)[0], None)
        c1, c2 = [0], [0]
        ex.cover_branching(ex.ROADS, 4, c1)
        ex.cover_branching_better(ex.ROADS, 4, c2)
        self.assertEqual((c1[0], c2[0]), (31, 12))
        r = random.Random(32)
        for _ in range(200):
            vs = list(range(r.randint(1, 8)))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.4]
            k = r.randint(0, 5)
            want = ex.cover_brute(vs, es, k)[0] is not None
            for solver in (lambda: ex.cover_branching(es, k, [0]), lambda: ex.cover_branching_better(es, k, [0]),
                           lambda: ex.cover_with_kernel(es, k)):
                got = solver()
                self.assertEqual(got is not None, want)
                if got is not None:
                    self.assertTrue(len(set(got)) <= k and all(a in got or b in got for a, b in es))

    def test_branch_and_bound_and_dpll(self) -> None:
        self.assertEqual(ex.knapsack_branch_and_bound(ex.SHELF_VALUES, ex.SHELF_WEIGHTS, 20), (3658, [0, 3, 4, 8, 9], 11))
        r = random.Random(33)
        for _ in range(200):
            n = r.randint(1, 9)
            vals = [r.randint(1, 100) for _ in range(n)]
            wts = [r.randint(1, 10) for _ in range(n)]
            cap = r.randint(0, 30)
            best = max((sum(v for v, b in zip(vals, bits) if b) for bits in itertools.product([0, 1], repeat=n)
                        if sum(w for w, b in zip(wts, bits) if b) <= cap), default=0)
            self.assertEqual(ex.knapsack_branch_and_bound(vals, wts, cap)[0], best)
        for _ in range(300):
            n = r.randint(3, 8)
            f = ex.random_3sat(n, r.randint(1, 40), r)
            res = ex.dpll(f)
            self.assertEqual(res is not None, ex.brute_sat(f, n))
            if res:
                self.assertTrue(all(any(res.get(abs(l), False) == (l > 0) for l in c) for c in f))
        self.assertEqual((ex.dpll([]), ex.dpll([[1], [-1]])), ({}, None))
        st = {}
        self.assertEqual((ex.dpll([[1, 2], [-1, 3], [-1, -3], [-2, 3]], stats=st), st), ({1: False, 2: True, 3: True}, {"decisions": 2, "units": 3}))
        st = {}
        f = ex.random_3sat(30, 120, random.Random(9))
        self.assertIsNotNone(ex.dpll(f, stats=st))
        self.assertEqual(st, {"decisions": 17, "units": 52})


if __name__ == "__main__":
    unittest.main()
