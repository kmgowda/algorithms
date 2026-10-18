import random
import statistics
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestPatterns(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(0, 100) for _ in range(rng.randint(1, 30))]
            k = rng.randint(1, len(v))
            self.assertEqual(ex.top_k(v, k), sorted(v, reverse=True)[:k])
            lists = [sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 5))]
            self.assertEqual(ex.k_way_merge(lists), sorted(x for l in lists for x in l))
            self.assertEqual(list(ex.medians_of_stream(v)), [statistics.median(v[:i + 1]) for i in range(len(v))])
        with self.assertRaises(ValueError):
            ex.RunningMedian().median()

    def test_shops(self) -> None:
        self.assertEqual(ex.k_closest_shops([("Bakery", 3, 4), ("Pharmacy", 1, 1), ("Bookshop", -2, 2), ("Florist", 6, 1)], 2),
                         ["Pharmacy", "Bookshop"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.top_k_frequent("the lion and the zebra and the bird".split(), 2), ["the", "and"])
        self.assertEqual(sol.kth_smallest_in_sorted_rows([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8), 13)
        self.assertEqual(sol.min_meeting_rooms([(9, 10), (9, 12), (11, 13), (13, 14)]), 2)
        rng = random.Random(2)
        for _ in range(100):
            m = []
            for _ in range(rng.randint(0, 8)):
                s = rng.randint(0, 20)
                m.append((s, s + rng.randint(1, 5)))
            brute = max([sum(1 for s, e in m if s <= t < e) for t in range(0, 30)] + [0])
            self.assertEqual(sol.min_meeting_rooms(m), brute)
        self.assertEqual(sol.sliding_median([1, 3, -1, -3, 5, 3], 3), [1, -1, -1, 3])


if __name__ == "__main__":
    unittest.main()
