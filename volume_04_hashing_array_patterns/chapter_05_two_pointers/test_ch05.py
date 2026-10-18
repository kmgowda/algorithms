import itertools
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestTwoPointers(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = sorted(rng.randint(-10, 10) for _ in range(rng.randint(0, 10)))
            t = rng.randint(-15, 15)
            r = ex.pair_with_sum_sorted(v, t)
            exists = any(v[i] + v[j] == t for i, j in itertools.combinations(range(len(v)), 2))
            self.assertEqual(r is not None, exists)
            if r:
                self.assertEqual(v[r[0]] + v[r[1]], t)
            triples = sorted({tuple(sorted(c)) for c in itertools.combinations(v, 3) if sum(c) == 0})
            self.assertEqual(sorted(ex.three_sum_zero(v)), triples)
            h = [rng.randint(0, 9) for _ in range(rng.randint(2, 10))]
            self.assertEqual(ex.max_water(h), max(min(h[i], h[j]) * (j - i) for i, j in itertools.combinations(range(len(h)), 2)))
            self.assertEqual(sol.trapped_rain(h), sum(max(min(max(h[:i + 1]), max(h[i:])) - h[i], 0) for i in range(len(h))))

    def test_read_write_and_merge(self) -> None:
        r = [12, 3, 25, 8, 30]
        n = ex.compact_valid_readings(r, 10)
        self.assertEqual(r[:n], [12, 25, 30])
        self.assertEqual(ex.merge_sorted_schedules([600, 715, 900], [630, 800]), [600, 630, 715, 800, 900])
        self.assertTrue(ex.is_subsequence("zoo", "zebra on tour"))
        self.assertFalse(ex.is_subsequence("ozz", "zoo"))
        self.assertTrue(ex.is_subsequence("", "abc"))

    def test_boats(self) -> None:
        self.assertEqual(ex.boats_needed([3, 2, 2, 1], 3), 3)
        self.assertEqual(ex.boats_needed([1, 2], 3), 1)
        self.assertEqual(ex.boats_needed([], 3), 0)


class TestSolutions(unittest.TestCase):
    def test_colors(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            c = [rng.randint(0, 2) for _ in range(rng.randint(0, 15))]
            expected = sorted(c)
            sol.sort_colors(c)
            self.assertEqual(c, expected)

    def test_closest_and_dupes(self) -> None:
        a, b = [1, 4, 5, 7], [10, 20, 30, 40]
        best = sol.closest_pair_sum(a, b, 32)
        self.assertEqual(abs(sum(best) - 32), min(abs(x + y - 32) for x in a for y in b))
        v = [1, 1, 1, 2, 2, 3]
        self.assertEqual(v[:sol.remove_duplicates_keep_two(v)], [1, 1, 2, 2, 3])
        self.assertEqual(sol.trapped_rain([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)


if __name__ == "__main__":
    unittest.main()
