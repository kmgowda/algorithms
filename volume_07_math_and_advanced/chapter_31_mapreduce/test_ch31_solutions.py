import random
import statistics
import unittest

import ch31_examples as ex
from ch31_solutions import branch_stats


class TestBranchStats(unittest.TestCase):
    def test_loans(self) -> None:
        stats, sent = branch_stats(ex.LOANS)
        self.assertEqual(stats["East"], (1, 14.0, 0.0))
        n, mean, var = stats["North"]
        self.assertEqual((n, mean, sent), (5, 2.0, 4))
        self.assertAlmostEqual(var, 0.4)

    def test_shuffle_is_machines_times_keys(self) -> None:
        stats, sent = branch_stats(ex.LOANS * 1000, machines=10)
        self.assertEqual((stats["North"][:2], sent), ((5000, 2.0), 15))          # at most 10 machines x 2 branches

    def test_smallest(self) -> None:
        self.assertEqual(branch_stats([]), ({}, 0))
        self.assertEqual(branch_stats([("West", 7)], machines=1), ({"West": (1, 7.0, 0.0)}, 1))
        with self.assertRaises(ValueError):
            branch_stats([("West", 7)], machines=0)

    def test_random_against_direct(self) -> None:
        r = random.Random(31)
        for _ in range(100):
            recs = [(r.choice("NES"), r.randint(0, 20)) for _ in range(r.randint(1, 30))]
            stats, _ = branch_stats(recs, r.randint(1, 6))
            for b, (n, mean, var) in stats.items():
                xs = [x for k, x in recs if k == b]
                self.assertEqual(n, len(xs))
                self.assertAlmostEqual(mean, statistics.fmean(xs))
                self.assertAlmostEqual(var, statistics.pvariance(xs))


if __name__ == "__main__":
    unittest.main()
