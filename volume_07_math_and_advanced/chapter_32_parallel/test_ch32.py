import itertools
import random
import unittest

import ch32_examples as ex


class TestChapter29(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.tree_sum(list(range(1, 17))), ex.tree_sum(list(range(1, 1025)))[1:]), ((136, 15, 4), (1023, 10)))
        self.assertEqual(ex.prefix_sums_parallel([3, 1, 4, 1, 5, 9, 2, 6]), ([3, 4, 8, 9, 14, 23, 25, 31], 17, 3))
        self.assertEqual([round(ex.time_with_helpers(1023, 10, p), 1) for p in (1, 4, 32, 1024)], [1033.0, 265.8, 42.0, 11.0])
        self.assertEqual([round(ex.amdahl(0.9, p), 2) for p in (2, 8, 64, 1000)], [1.82, 4.71, 8.77, 9.91])

    def test_every_case(self) -> None:
        self.assertEqual((ex.tree_sum([]), ex.tree_sum([7]), ex.tree_sum([1, 2, 3])), ((0, 0, 0), (7, 0, 0), (6, 2, 2)))
        self.assertEqual((ex.prefix_sums_parallel([]), ex.prefix_sums_parallel([5])), (([], 0, 0), ([5], 0, 0)))
        self.assertEqual((ex.amdahl(1.0, 8), ex.amdahl(0.0, 8)), (8.0, 1.0))
        r = random.Random(29)
        for _ in range(200):
            v = [r.randint(-9, 9) for _ in range(r.randint(1, 40))]
            total, work, rounds = ex.tree_sum(v)
            self.assertEqual((total, work), (sum(v), len(v) - 1))
            self.assertEqual(ex.prefix_sums_parallel(v)[0], list(itertools.accumulate(v)))


class TestDepth(unittest.TestCase):
    def test_dag_and_scheduler(self) -> None:
        import math
        dag = ex.tree_sum_dag(16)
        W, S = ex.work_span(dag)
        self.assertEqual((W, S), (31, 5))
        self.assertEqual([ex.greedy_schedule(dag, p) for p in (1, 2, 4, 8, 16)], [31, 18, 11, 7, 5])
        for n in range(0, 40):
            dag = ex.tree_sum_dag(n)
            W, S = ex.work_span(dag)
            for p in (1, 2, 3, 5, 8):
                t = ex.greedy_schedule(dag, p)
                self.assertGreaterEqual(t, max(math.ceil(W / p) if W else 0, S))       # work law and span law
                self.assertLessEqual(t, W / p + S + 1e-9)                               # Brent's bound

    def test_race_scan_merge(self) -> None:
        self.assertEqual((ex.race_outcomes(1, 2), ex.race_outcomes(2, 2)), ({2: 2, 1: 4}, {4: 6, 3: 32, 2: 32}))
        self.assertEqual(ex.blelloch_scan([3, 1, 4, 1, 5, 9, 2, 6]), ([0, 3, 4, 8, 9, 14, 23, 25], 14, 6, [3, 4, 4, 9, 5, 14, 2, 31]))
        self.assertEqual((ex.blelloch_scan([]), ex.blelloch_scan([7])[0]), (([], 0, 0, []), [0]))
        import random
        r = random.Random(37)
        for _ in range(200):
            v = [r.randint(-9, 9) for _ in range(r.randint(0, 20))]
            run, acc = [], 0
            for x in v:
                run.append(acc)
                acc += x
            self.assertEqual(ex.blelloch_scan(v)[0], run)
            a, b = sorted(r.sample(range(100), r.randint(0, 10))), sorted(r.sample(range(100), r.randint(0, 10)))
            self.assertEqual(ex.parallel_merge(a, b), sorted(a + b))
        m = ex.merge_spans(1_000_000)
        self.assertEqual((m["span serial merge"], m["span parallel merge"], m["parallelism serial"], m["parallelism parallel"]),
                         (1999993, 3648, 10.0, 5464))


if __name__ == "__main__":
    unittest.main()
