import math
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


def disc_points(n: int, seed: int) -> list:
    rng, pts = random.Random(seed), []
    while len(pts) < n:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y < 1:
            pts.append((x, y))
    return pts


class TestThinkingProblems(unittest.TestCase):
    def test_bounded_density(self) -> None:                   # Thinking Problem 1
        n = 10_000
        even = sol.expected_sum_of_squares([1 / n] * n, n)
        self.assertAlmostEqual(even, 2 * n - 1, places=3)
        linear = sol.expected_sum_of_squares(sol.linear_density_buckets(n), n)
        self.assertAlmostEqual(linear, 23_332, delta=1)
        self.assertLessEqual(linear, n * (1 + 2))               # the bound n(1 + c) with c = 2
        self.assertAlmostEqual(sum(sol.linear_density_buckets(n)), 1.0)
        self.assertTrue(all(q <= 2 / n for q in sol.linear_density_buckets(n)))
        bunched = sol.expected_sum_of_squares(sol.power_eight_buckets(n), n)
        self.assertGreater(bunched, 10_000_000)
        self.assertAlmostEqual(n * sol.power_eight_buckets(n)[0], 3162.28, places=1)
        self.assertEqual(sol.expected_sum_of_squares([1.0], 1), 1.0)

    def test_sort_by_distance(self) -> None:                  # Thinking Problem 2
        self.assertEqual(sol.sort_by_distance([]), [])
        self.assertEqual(sol.sort_by_distance([(0.3, 0.4)]), [(0.3, 0.4)])
        self.assertEqual(sol.sort_by_distance([(0.5, 0.5), (0.1, 0.0), (0.0, -0.9)]),
                         [(0.1, 0.0), (0.5, 0.5), (0.0, -0.9)])
        ties = [(0.6, 0.0), (0.0, 0.6), (-0.6, 0.0)]            # equal distances keep their order
        self.assertEqual(sol.sort_by_distance(ties), ties)
        self.assertEqual(sol.sort_by_distance([(1.0, 0.0), (0.0, 0.0)]), [(0.0, 0.0), (1.0, 0.0)])
        for seed in range(20):
            pts = disc_points(random.Random(seed).randint(0, 200), seed)
            self.assertEqual(sol.sort_by_distance(pts), sorted(pts, key=lambda p: p[0] ** 2 + p[1] ** 2))
        pts = disc_points(10_000, 5)
        sizes = [0] * 10_000
        for x, y in pts:
            sizes[min(int((x * x + y * y) * 10_000), 9_999)] += 1
        self.assertEqual((max(sizes), sum(s * s for s in sizes)), (7, 19_754))

    def test_leo_flaw(self) -> None:                          # Thinking Problem 3
        self.assertEqual((sol.leo_prediction(2, 2), sol.exact_average_sum_of_squares(2, 2)), (2.0, 3.0))
        for n in (1, 2, 3, 4):
            self.assertAlmostEqual(sol.exact_average_sum_of_squares(n, n), 2 * n - 1)
        log = {}
        ex.bucket_sort([47] * 9, 0, 100, 9, log)
        self.assertEqual((sum(len(b) ** 2 for b in log["buckets"]), log["comparisons"]), (81, 8))
        log = {}
        ex.bucket_sort(list(range(9, 0, -1)), 0, 100, 9, log)
        self.assertEqual((sum(len(b) ** 2 for b in log["buckets"]), log["comparisons"]), (81, 36))
        self.assertEqual(sol.leo_prediction(9, 9), 9.0)
        self.assertTrue(math.isclose(sol.leo_prediction(0, 3), 0.0))


if __name__ == "__main__":
    unittest.main()
