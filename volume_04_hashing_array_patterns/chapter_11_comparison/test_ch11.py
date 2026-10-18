import random
import timeit
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestComparison(unittest.TestCase):
    def test_pair_methods_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-10, 10) for _ in range(rng.randint(0, 10))]
            t = rng.randint(-15, 15)
            expected = ex.pair_brute(v, t)
            self.assertEqual(ex.pair_hash(v, t), expected)
            self.assertEqual(ex.pair_sort_two_pointers(v, t), expected)

    def test_hash_beats_brute_at_scale(self) -> None:
        data = list(range(2000))
        brute = min(timeit.repeat(lambda: ex.pair_brute(data, -1), number=1, repeat=1))
        hashed = min(timeit.repeat(lambda: ex.pair_hash(data, -1), number=1, repeat=1))
        self.assertLess(hashed, brute)

    def test_membership(self) -> None:
        t = ex.membership_times(5000, lookups=500)
        self.assertLess(t["set (hashing)"], t["list (linear scan)"])
        self.assertLess(t["sorted list (binary search)"], t["list (linear scan)"])

    def test_chooser(self) -> None:
        self.assertEqual(ex.choose_technique("pair or complement"), "hash map of seen values")
        self.assertEqual(ex.choose_technique("pair or complement", sorted_input=True), "two pointers")
        self.assertEqual(ex.choose_technique("longest or shortest consecutive stretch", negatives=True),
                         "prefix sums + hash map")
        self.assertTrue(ex.choose_technique("something new").startswith("write the brute force"))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            v = [rng.randint(-4, 6) for _ in range(rng.randint(0, 10))]
            a, b, c = sol.has_duplicate_three_ways(v)
            self.assertTrue(a == b == c)
            nonneg = [abs(x) for x in v]
            lim = rng.randint(0, 12)
            brute = max([j - i for i in range(len(nonneg) + 1) for j in range(i, len(nonneg) + 1)
                         if sum(nonneg[i:j]) <= lim] + [0])
            self.assertEqual(sol.longest_stretch_sum_at_most(nonneg, lim), brute)
            t = rng.randint(-5, 5)
            brute_exact = max([j - i for i in range(len(v) + 1) for j in range(i + 1, len(v) + 1)
                               if sum(v[i:j]) == t] + [0])
            self.assertEqual(sol.longest_stretch_sum_exactly(v, t), brute_exact)


if __name__ == "__main__":
    unittest.main()
