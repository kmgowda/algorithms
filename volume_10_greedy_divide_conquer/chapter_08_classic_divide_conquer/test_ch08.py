import random
import unittest
from collections import Counter

import ch08_examples as ex
import ch08_solutions as sol


class TestClassicDC(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(0, 9) for _ in range(rng.randint(1, 30))]
            mx, mn, comps = ex.max_min(v)
            self.assertEqual((mx, mn), (max(v), min(v)))
            if len(v) >= 4:
                self.assertLess(comps, 2 * len(v) - 2)                 # beats max and min found separately
            if len(v) in (2, 4, 8, 16):
                self.assertEqual(comps, 3 * len(v) // 2 - 2)            # exact for powers of two
            brute = sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j])
            inv, merged = ex.count_inversions(v)
            self.assertEqual((inv, merged), (brute, sorted(v)))
            self.assertEqual(sol.reverse_pairs(v), sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > 2 * v[j]))
            top, c = Counter(v).most_common(1)[0]
            expected = top if c * 2 > len(v) else None
            self.assertEqual(ex.majority(v), expected)
            self.assertEqual(sol.boyer_moore_majority(v), expected)
            pts = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(rng.randint(2, 40))]
            self.assertAlmostEqual(ex.closest_pair(pts), ex.closest_pair_brute(pts))
            a, b = sorted(rng.sample(range(100), 5)), sorted(rng.sample(range(100), 6))
            k = rng.randint(1, 11)
            self.assertEqual(sol.kth_smallest_two_sorted(a, b, k), sorted(a + b)[k - 1])
            p = sol.peak_index(v)
            self.assertTrue((p == 0 or v[p] >= v[p - 1]) and (p == len(v) - 1 or v[p] >= v[p + 1]))

    def test_examples(self) -> None:
        self.assertEqual(ex.count_inversions([2, 4, 1, 3, 5])[0], 3)
        self.assertEqual(ex.ranking_disagreement(["Jaws", "Up", "Cars", "Coco"], ["Up", "Coco", "Jaws", "Cars"]), 3)
        self.assertEqual(ex.max_min([31, 28, 35, 22, 40, 19, 33, 27]), (40, 19, 10))


if __name__ == "__main__":
    unittest.main()
