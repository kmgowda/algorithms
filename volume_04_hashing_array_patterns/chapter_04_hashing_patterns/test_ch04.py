import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestPatterns(unittest.TestCase):
    def test_two_sum(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            p = [rng.randint(1, 30) for _ in range(rng.randint(0, 10))]
            t = rng.randint(2, 50)
            r = ex.two_sum(p, t)
            exists = any(p[i] + p[j] == t for i in range(len(p)) for j in range(i + 1, len(p)))
            self.assertEqual(r is not None, exists)
            if r:
                i, j = r
                self.assertTrue(i < j and p[i] + p[j] == t)

    def test_brute_force_matches(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            v = [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]
            t = rng.randint(-6, 6)
            brute = sum(1 for i in range(len(v)) for j in range(i, len(v)) if sum(v[i:j + 1]) == t)
            self.assertEqual(ex.subarrays_with_sum(v, t), brute)
            k = rng.randint(1, 3)
            pairs = sum(1 for i, j in itertools.combinations(range(len(v)), 2) if abs(v[i] - v[j]) == k)
            self.assertEqual(ex.count_pairs_with_difference(v, k), pairs)
            days = [rng.randint(0, 15) for _ in range(rng.randint(0, 10))]
            s, best = set(days), 0
            for d in s:
                n = 0
                while d + n in s:
                    n += 1
                best = max(best, n)
            self.assertEqual(ex.longest_streak(days), best)
            res = [rng.choice("WL") for _ in range(rng.randint(0, 12))]
            brute_run = max([j - i for i in range(len(res) + 1) for j in range(i, len(res) + 1)
                             if res[i:j].count("W") == res[i:j].count("L")] + [0])
            self.assertEqual(ex.longest_balanced_run(res), brute_run)

    def test_fraud(self) -> None:
        tx = [("c1", 500), ("c2", 80), ("c1", -500), ("c2", -80)]
        self.assertEqual(ex.fraud_pairs(tx, 2), [("c1", 500), ("c2", 80)])
        self.assertEqual(ex.fraud_pairs(tx, 1), [])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.contains_nearby_duplicate([1, 2, 3, 1], 3))
        self.assertFalse(sol.contains_nearby_duplicate([1, 2, 3, 1], 2))
        self.assertEqual(sol.subarray_sum_divisible([4, 5, 0, -2, -3, 1], 5), 7)
        self.assertTrue(sol.isomorphic("egg", "add"))
        self.assertFalse(sol.isomorphic("foo", "bar"))
        self.assertFalse(sol.isomorphic("ab", "aa"))
        self.assertEqual(sol.four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2]), 2)


if __name__ == "__main__":
    unittest.main()
