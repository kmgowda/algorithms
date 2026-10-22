import heapq
import random
import statistics
import unittest

import ch15_examples as ex


class TestChapter55(unittest.TestCase):
    def test_every_case(self) -> None:
        for a, swaps, out in [([], 0, []), ([7], 0, [7]), ([1, 2, 3, 4, 5, 6, 7], 0, [1, 2, 3, 4, 5, 6, 7]),
                              ([7, 6, 5, 4, 3, 2, 1], 4, [1, 3, 2, 4, 6, 7, 5]), ([3, 3, 3], 0, [3, 3, 3])]:
            b = list(a)
            self.assertEqual((ex.heapify(b), b), (swaps, out))
        s = [58, 25, 91, 12, 70, 47, 84, 31, 63]
        self.assertEqual([ex.top_k(s, k) for k in (3, 0, 20)], [[91, 84, 70], [], sorted(s, reverse=True)])
        self.assertEqual((ex.top_k([], 3), ex.top_k([5, 5, 5, 1], 2)), ([], [5, 5]))
        self.assertEqual([ex.merge_k(x) for x in ([], [[], []], [[1, 2, 3]], [[1, 4], [2, 5], [3, 6]], [[1, 1], [1]])],
                         [[], [], [1, 2, 3], [1, 2, 3, 4, 5, 6], [1, 1, 1]])
        m = ex.RunningMedian()
        with self.assertRaises(IndexError):
            m.median()
        out = []
        for x in (5, 1, 9, 3, 3):
            m.add(x)
            out.append(m.median())
        self.assertEqual(out, [5, 3.0, 5, 4.0, 3])

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

    def test_new_techniques(self) -> None:
        self.assertEqual([ex.height_sum(n) for n in (0, 1, 2, 7, 15, 31)], [0, 0, 1, 4, 11, 26])
        for n in range(0, 200):
            self.assertEqual(ex.height_sum(n), n - bin(n).count("1"))
            a = list(range(n, 0, -1))
            self.assertLessEqual(ex.heapify(a), ex.height_sum(n))
        self.assertEqual(ex.heapify(list(range(15, 0, -1))), 11)
        self.assertEqual(ex.k_smallest([7, 2, 9, 4, 1, 8], 3), [1, 2, 4])
        self.assertEqual((ex.k_smallest([], 3), ex.k_smallest([5, 1], 0), ex.k_smallest([3, 3, 1], 2)), ([], [], [1, 3]))
        self.assertEqual(ex.join_cost([4, 3, 2, 6]), (29, [(2, 3, 5), (4, 5, 9), (6, 9, 15)]))
        self.assertEqual(ex.join_cost([1, 2, 3, 4])[0], 19)
        self.assertEqual((ex.join_cost([]), ex.join_cost([7])), ((0, []), (0, [])))
        rng = random.Random(2)
        for _ in range(100):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 12))]
            k = rng.randint(0, 5)
            self.assertEqual(ex.k_smallest(a, k), sorted(a)[:k])

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
