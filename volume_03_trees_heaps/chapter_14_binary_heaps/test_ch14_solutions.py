import itertools
import random
import unittest

import ch14_examples as ex
import ch14_solutions as sol


class TestChapter14Solutions(unittest.TestCase):
    def test_push_build_worst(self) -> None:
        self.assertEqual([sol.push_build_worst(n) for n in range(0, 9)], [0, 0, 1, 2, 4, 6, 8, 10, 13])
        for n in range(1, 200):
            self.assertEqual(len(ex.MinHeap(range(n, 0, -1)).trace), sol.push_build_worst(n))
        for n in range(1, 8):                                  # no order of n distinct keys costs more
            worst = max(len(ex.MinHeap(p).trace) for p in itertools.permutations(range(n)))
            self.assertEqual(worst, sol.push_build_worst(n))

    def test_kth_smallest(self) -> None:
        self.assertEqual(sol.kth_smallest([7], 1), 7)
        for bad in (0, 2):
            with self.assertRaises(IndexError):
                sol.kth_smallest([7], bad)
        with self.assertRaises(IndexError):
            sol.kth_smallest([], 1)
        pile = [12, 25, 47, 31, 70, 91, 84, 58, 63]
        self.assertEqual([sol.kth_smallest(pile, k) for k in range(1, 10)], sorted(pile))
        rng = random.Random(2)
        for _ in range(200):
            items = [rng.randint(0, 20) for _ in range(rng.randint(1, 30))]
            a = ex.MinHeap(items).a
            k = rng.randint(1, len(a))
            before = list(a)
            self.assertEqual(sol.kth_smallest(a, k), sorted(items)[k - 1])
            self.assertEqual(a, before)

    def test_left_first_pop_breaks_the_heap(self) -> None:
        a = [7]
        self.assertEqual((sol.pop_first_smaller_child(a), a), (7, []))
        a = [1, 5, 3, 9]
        self.assertEqual(sol.pop_first_smaller_child(a), 1)
        self.assertEqual(a, [5, 9, 3])
        self.assertFalse(ex.is_heap(a))


if __name__ == "__main__":
    unittest.main()
