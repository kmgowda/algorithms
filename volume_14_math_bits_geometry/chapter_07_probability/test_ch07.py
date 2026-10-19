import math
import random
import unittest
from collections import Counter

import ch07_examples as ex
import ch07_solutions as sol


class TestProbability(unittest.TestCase):
    def test_distributions(self) -> None:
        rng = random.Random(1)
        trials = 30000
        fy = Counter(tuple(ex.fisher_yates([1, 2, 3], rng)) for _ in range(trials))
        self.assertEqual(len(fy), 6)
        self.assertTrue(all(abs(c - trials / 6) < 0.05 * trials / 6 for c in fy.values()))
        bad = Counter(tuple(ex.naive_shuffle([1, 2, 3], rng)) for _ in range(trials))
        self.assertGreater(max(bad.values()) / min(bad.values()), 1.15)
        res = Counter(x for _ in range(trials) for x in ex.reservoir_sample(range(10), 3, rng))
        self.assertTrue(all(abs(c - trials * 3 / 10) < 0.05 * trials * 3 / 10 for c in res.values()))
        picks = Counter(sol.random_pick_index([1, 3, 2, 3, 3], 3, rng) for _ in range(trials))
        self.assertEqual(set(picks), {1, 3, 4})
        self.assertTrue(all(abs(c - trials / 3) < 0.05 * trials / 3 for c in picks.values()))
        w = Counter(sol.weighted_choice({"a": 1, "b": 3}, rng) for _ in range(trials))
        self.assertAlmostEqual(w["b"] / trials, 0.75, delta=0.02)
        self.assertEqual(sorted(ex.fisher_yates(list(range(20)), rng)), list(range(20)))

    def test_values(self) -> None:
        rng = random.Random(2)
        self.assertEqual(ex.expected_value({v: 1 / 6 for v in range(1, 7)}), 3.5)
        self.assertAlmostEqual(ex.simulate_mean(lambda r: r.randint(1, 6), 50000, rng), 3.5, delta=0.05)
        self.assertAlmostEqual(ex.monte_carlo_pi(200000, rng), math.pi, delta=0.02)
        self.assertAlmostEqual(ex.birthday_collision(23), 0.507, places=3)
        self.assertEqual(ex.birthday_collision(366), 1.0)
        self.assertAlmostEqual(sol.coupon_collector(6), 14.7, places=1)
        sim = sum(self._collect(6, rng) for _ in range(20000)) / 20000
        self.assertAlmostEqual(sim, sol.coupon_collector(6), delta=0.3)
        self.assertEqual(len(ex.ab_test_sample(list(range(1000)), 10, rng)), 100)

    @staticmethod
    def _collect(n, rng):
        seen, draws = set(), 0
        while len(seen) < n:
            seen.add(rng.randrange(n))
            draws += 1
        return draws


if __name__ == "__main__":
    unittest.main()
