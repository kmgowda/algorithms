import random
import statistics
import unittest

import ch07_examples as ex


class TestChapter07(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(len(ex.inversions(ex.PILE)), 17)
        self.assertEqual((ex.median(ex.PILE), ex.closest_pair(ex.PILE)), (58, (58, 63)))
        self.assertEqual(len(ex.inversions([3, 1, 2])), 2)
        self.assertEqual(len(ex.inversions([4, 3, 2, 1])), 6)
        self.assertEqual(ex.median([9, 2, 7, 4, 5, 1]), 4.5)
        self.assertEqual(ex.closest_pair([15, 3, 9, 8, 20]), (8, 9))
        self.assertEqual([n for n, _ in ex.stable_sort_demo()], ["Ana", "Eva", "Dev", "Ben", "Cai"])

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 60) for _ in range(rng.randint(2, 15))]
            dup = any(a[i] == a[j] for i in range(len(a)) for j in range(i + 1, len(a)))
            gap = min(abs(a[i] - a[j]) for i in range(len(a)) for j in range(i + 1, len(a)))
            d, (x, y) = ex.overdue_pairs(a)
            self.assertEqual(d, dup)
            self.assertEqual(y - x, gap)
            self.assertEqual(ex.median(a), statistics.median(a))
            self.assertTrue(ex.is_sorted(sorted(a)))


if __name__ == "__main__":
    unittest.main()
