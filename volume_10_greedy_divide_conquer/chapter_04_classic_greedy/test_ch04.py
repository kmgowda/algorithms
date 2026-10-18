import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def non_overlapping(ivs):
    s = sorted(ivs, key=lambda x: x[0])
    return all(a[1] <= b[0] for a, b in zip(s, s[1:]))


class TestClassicGreedy(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            n = rng.randint(0, 7)
            ivs = []
            for i in range(n):
                s = rng.randint(0, 12)
                ivs.append((f"e{i}", s, s + rng.randint(1, 4)))
            best = max((r for r in range(n + 1) for c in itertools.combinations(ivs, r)
                        if non_overlapping([(s, e) for _, s, e in c])), default=0)
            self.assertEqual(len(ex.activity_selection(ivs)), best)
            plain = [(s, e) for _, s, e in ivs]
            overlap = max([sum(1 for s, e in plain if s <= t < e) for t in range(20)] + [0])
            self.assertEqual(ex.rooms_needed(plain), overlap)
            self.assertEqual(sol.erase_overlaps(plain), n - best)

    def test_job_sequencing(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            jobs = [(f"j{i}", rng.randint(1, 4), rng.randint(1, 50)) for i in range(rng.randint(0, 6))]
            best = 0
            for r in range(len(jobs) + 1):
                for c in itertools.combinations(jobs, r):
                    ds = sorted(d for _, d, _ in c)
                    if all(d >= k + 1 for k, d in enumerate(ds)):
                        best = max(best, sum(p for _, _, p in c))
            self.assertEqual(ex.job_sequencing(jobs)[0], best)

    def test_fractional(self) -> None:
        total, taken = ex.fractional_knapsack([("saffron", 1, 60), ("pepper", 3, 90), ("cumin", 2, 30)], 3)
        self.assertAlmostEqual(total, 120)
        self.assertEqual(taken, {"saffron": 1, "pepper": 2})
        self.assertTrue(ex.is_canonical([1, 2, 5, 10, 20, 50]))
        self.assertFalse(ex.is_canonical([1, 3, 4]))

    def test_solutions(self) -> None:
        self.assertEqual(sol.min_arrows([(10, 16), (2, 8), (1, 6), (7, 12)]), 2)
        self.assertEqual(sol.merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]), [(1, 6), (8, 10), (15, 18)])
        self.assertEqual(sol.min_platforms([900, 940, 950, 1100], [910, 1200, 1120, 1130]), 3)


if __name__ == "__main__":
    unittest.main()
