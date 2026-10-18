import random
import sys
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestQuicksort(unittest.TestCase):
    def test_partition(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]
            original = sorted(a)
            p = ex.partition_lomuto(a, 0, len(a) - 1)
            self.assertTrue(all(x < a[p] for x in a[:p]))
            self.assertTrue(all(x >= a[p] for x in a[p + 1:]))
            self.assertEqual(sorted(a), original)

    def test_sorts(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            v = [rng.randint(-10, 10) for _ in range(rng.randint(0, 40))]
            for sort in (lambda a: ex.quicksort(a, rng=random.Random(3)),
                         lambda a: ex.quicksort_three_way(a, rng=random.Random(3)),
                         sol.quicksort_hoare, sol.quicksort_median3):
                a = list(v)
                sort(a)
                self.assertEqual(a, sorted(v))

    def test_worst_case_shape(self) -> None:
        n = 200
        self.assertEqual(ex.quicksort_first_pivot_comparisons(list(range(n))), n * (n - 1) // 2)
        self.assertLess(ex.quicksort_first_pivot_comparisons(random.Random(4).sample(range(n), n)), n * (n - 1) // 4)

    def test_random_pivot_handles_sorted_and_equal(self) -> None:
        a = list(range(20_000))
        ex.quicksort(a, rng=random.Random(5))
        self.assertEqual(a, sorted(a))
        b = [7] * 20_000
        ex.quicksort_three_way(b, rng=random.Random(5))
        self.assertEqual(b, [7] * 20_000)

    def test_ratings(self) -> None:
        r = [5, 3, 5, 1, 4, 5, 2, 5, 3, 4]
        self.assertEqual(ex.sort_star_ratings(r), sorted(r))


class TestSolutions(unittest.TestCase):
    def test_predicate_and_median3(self) -> None:
        stock = ["milk:0", "eggs:5", "rice:0", "tea:3"]
        k = sol.partition_by_predicate(stock, lambda s: not s.endswith(":0"))
        self.assertEqual(sorted(stock[:k]), ["eggs:5", "tea:3"])
        self.assertEqual(sol.median_of_three([9, 1, 5], 0, 2), 2)
        self.assertEqual(sol.median_of_three([1, 5, 9], 0, 2), 1)


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    unittest.main()
