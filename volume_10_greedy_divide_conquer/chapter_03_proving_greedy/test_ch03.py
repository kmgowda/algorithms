import itertools
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def max_compatible(intervals):
    best = 0
    for r in range(len(intervals) + 1):
        for combo in itertools.combinations(sorted(intervals), r):
            if all(a[1] <= b[0] for a, b in zip(combo, combo[1:])):
                best = max(best, r)
    return best


class TestProofs(unittest.TestCase):
    def test_greedy_matches_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            n = rng.randint(1, 6)
            d = [rng.randint(1, 9) for _ in range(n)]
            self.assertEqual(ex.total_waiting(d, ex.shortest_first(d)), ex.brute_best(n, lambda o: ex.total_waiting(d, o)))
            jobs = [(rng.randint(1, 5), rng.randint(1, 15)) for _ in range(n)]
            self.assertEqual(ex.max_lateness(jobs, ex.earliest_deadline_first(jobs)),
                             ex.brute_best(n, lambda o: ex.max_lateness(jobs, o)))
            w = [rng.randint(1, 5) for _ in range(n)]
            self.assertEqual(sol.weighted_cost(d, w, sol.weighted_waiting_order(d, w)),
                             min(sol.weighted_cost(d, w, list(p)) for p in itertools.permutations(range(n))))
            ivs = []
            for _ in range(rng.randint(0, 7)):
                s = rng.randint(0, 10)
                ivs.append((s, s + rng.randint(1, 4)))
            chosen = ex.stays_ahead_activities(ivs)
            self.assertEqual(len(chosen), max_compatible(ivs))

    def test_examples(self) -> None:
        self.assertEqual(ex.bank_queue_plan({"Asha": 8, "Bilal": 2, "Chen": 5}), (["Bilal", "Chen", "Asha"], 24))
        self.assertEqual(sol.counterexample_longest_first([5, 1, 3]), (22, 14))   # longest first: 5 + 8 + 9
        self.assertEqual(sol.find_inversion([2, 0, 1], [6, 8, 9]), (2, 0))
        self.assertIsNone(sol.find_inversion([0, 1, 2], [6, 8, 9]))


if __name__ == "__main__":
    unittest.main()
