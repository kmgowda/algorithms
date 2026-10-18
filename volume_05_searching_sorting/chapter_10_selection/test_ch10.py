import random
import statistics
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestSelection(unittest.TestCase):
    def test_all_methods_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-20, 20) for _ in range(rng.randint(1, 40))]
            k = rng.randint(1, len(v))
            expected = sorted(v)[k - 1]
            self.assertEqual(ex.kth_smallest_by_sorting(v, k), expected)
            self.assertEqual(ex.quickselect(v, k, random.Random(2)), expected)
            self.assertEqual(ex.median_of_medians(v, k), expected)
            self.assertEqual(ex.median(v), statistics.median(v))
        with self.assertRaises(ValueError):
            ex.quickselect([1], 2)
        with self.assertRaises(ValueError):
            ex.median([])

    def test_quickselect_does_not_modify(self) -> None:
        v = [5, 3, 1]
        ex.quickselect(v, 1)
        self.assertEqual(v, [5, 3, 1])

    def test_industry(self) -> None:
        times = list(range(1, 101))
        self.assertEqual(ex.p95_latency(times), 95)
        self.assertEqual(ex.closest_shops([("Bakery", 3, 4), ("Pharmacy", 1, 1), ("Bookshop", -2, 2), ("Florist", 6, 1)], 2),
                         ["Pharmacy", "Bookshop"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.kth_largest([3, 2, 1, 5, 6, 4], 2), 5)
        self.assertEqual(sol.top_k_frequent("the lion and the zebra and the bird".split(), 2), ["the", "and"])
        rng = random.Random(3)
        for _ in range(100):
            houses = [rng.randint(0, 50) for _ in range(rng.randint(1, 9))]
            m = sol.best_meeting_point(houses)
            best = min(sum(abs(h - p) for h in houses) for p in range(0, 51))
            self.assertEqual(sum(abs(h - m) for h in houses), best)
            w = sol.wiggle_sort([rng.randint(0, 9) for _ in range(rng.randint(0, 10))])
            self.assertTrue(all((w[i] <= w[i + 1]) if i % 2 == 0 else (w[i] >= w[i + 1]) for i in range(len(w) - 1)))


if __name__ == "__main__":
    unittest.main()
