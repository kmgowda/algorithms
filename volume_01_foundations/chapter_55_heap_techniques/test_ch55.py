import heapq
import random
import statistics
import unittest

import ch55_examples as ex


class TestChapter55(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            a = [rng.randint(0, 99) for _ in range(rng.randint(0, 40))]
            b = a[:]
            ex.heapify(b)
            self.assertTrue(all(b[(i - 1) // 2] <= b[i] for i in range(1, len(b))))
            self.assertEqual(sorted(b), sorted(a))
            k = rng.randint(1, 5)
            self.assertEqual(ex.top_k(a, k), sorted(a, reverse=True)[:k])
            lists = [sorted(rng.sample(range(100), rng.randint(0, 6))) for _ in range(rng.randint(1, 5))]
            self.assertEqual(ex.merge_k(lists), sorted(x for l in lists for x in l))
            rm = ex.RunningMedian()
            for i, x in enumerate(a):
                rm.add(x)
                self.assertEqual(rm.median(), statistics.median(a[:i + 1]))

    def test_examples(self) -> None:
        a = [70, 63, 58, 47, 31, 25, 12]
        ex.heapify(a)
        self.assertEqual(a, [12, 31, 25, 47, 63, 70, 58])
        b = [9, 4, 7, 1, 2, 6]
        ex.heapify(b)
        self.assertEqual(b, [1, 2, 6, 4, 9, 7])
        self.assertEqual(ex.top_k([72, 95, 41, 88, 60, 99, 77, 83], 3), [99, 95, 88])


if __name__ == "__main__":
    unittest.main()
