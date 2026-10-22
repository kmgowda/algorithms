import random
import unittest

import ch15_examples as ex
import ch15_solutions as sol


class TestFibonacciStack(unittest.TestCase):
    def test_small_and_large(self) -> None:
        self.assertEqual([sol.fibonacci_stack_bound(n) for n in (0, 1, 2, 3, 6, 7, 13, 14)],
                         [0, 1, 1, 2, 2, 3, 3, 4])
        self.assertEqual(sol.fibonacci_stack_bound(1_000_000), 26)

    def test_against_brute_force(self) -> None:
        def deepest(n, below=None, last=None):          # longest stack (top first) obeying the invariants
            best = 0
            for r in range(1, n + 1):
                if last is not None and r <= last:
                    continue
                if below is not None and r <= below + last:
                    continue
                best = max(best, 1 + deepest(n - r, last, r))
            return best
        for n in range(0, 30):
            self.assertEqual(sol.fibonacci_stack_bound(n), deepest(n), n)


class TestNaturalMergeSort(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        for a in ([], [7], [2, 1], [1, 2], [5, 5]):
            b = list(a)
            sol.natural_merge_sort(b)
            self.assertEqual(b, sorted(a))
        self.assertEqual(ex.count_comparisons(sol.natural_merge_sort, [])[1], 0)
        self.assertEqual(ex.count_comparisons(sol.natural_merge_sort, [7])[1], 0)

    def test_sorts_stably_within_bound(self) -> None:
        rng = random.Random(12)
        for _ in range(300):
            a = [rng.randint(0, 9) for _ in range(rng.randint(0, 60))]
            recs = [ex.Counted(v, [0]) for v in a]
            for i, c in enumerate(recs):
                c.tag = i
            sol.natural_merge_sort(recs)
            self.assertEqual([(c.key, c.tag) for c in recs], sorted((v, i) for i, v in enumerate(a)))
            r = len(ex.find_runs(list(a)))
            self.assertLessEqual(ex.count_comparisons(sol.natural_merge_sort, a)[1], sol.natural_bound(len(a), r))

    def test_staircase_numbers(self) -> None:
        c = sol.staircase_costs(160)
        self.assertEqual((c["n"], c["natural comparisons"], c["merge sort comparisons"]), (12880, 102031, 133668))
        self.assertEqual(sol.natural_bound(12880, 160), 115919)


class TestTeachingRule(unittest.TestCase):
    def test_staircase_trace(self) -> None:
        self.assertEqual(sol.staircase(4), [0, 4, 7, 9, 1, 5, 8, 2, 6, 3])
        self.assertEqual(sol.teaching_merges([4, 3, 2, 1]), [(2, 1), (3, 3), (4, 6)])
        self.assertEqual(sol.teaching_merges([]), [])
        self.assertEqual(sol.teaching_merges([5]), [])

    def test_cubic_growth(self) -> None:
        for k in (4, 40, 160):
            lengths = list(range(k, 0, -1))
            self.assertEqual(ex.merge_cost(sol.teaching_merges(lengths)), k * (k + 1) * (k + 2) // 6 - 1)
        rows = {k: sol.staircase_costs(k) for k in (4, 40, 160)}
        self.assertEqual([rows[k]["teaching copies"] for k in (4, 40, 160)], [19, 11479, 695519])
        self.assertEqual([rows[k]["Timsort copies"] for k in (4, 40, 160)], [24, 4411, 101664])
        self.assertEqual([rows[k]["teaching comparisons"] for k in (4, 40, 160)], [25, 12259, 708239])
        self.assertEqual([rows[k]["merge sort comparisons"] for k in (4, 40, 160)], [23, 6082, 133668])

    def test_teaching_merges_match_timsort(self) -> None:
        rng = random.Random(5)
        for _ in range(100):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 40))]
            b, log = list(a), []
            ex.timsort(b, log=log)
            lengths = [len(r) for r in log[0][1]] if log else []
            merged = [len(part) for kind, part in log[1:]]
            self.assertEqual(merged, [x + y for x, y in sol.teaching_merges(lengths)])


if __name__ == "__main__":
    unittest.main()
