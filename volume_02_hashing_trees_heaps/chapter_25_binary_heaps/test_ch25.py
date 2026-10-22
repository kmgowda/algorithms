import heapq
import random
import unittest

import ch25_examples as ex


class TestChapter54(unittest.TestCase):
    def test_every_case(self) -> None:
        for f in ("pop", "peek"):
            with self.assertRaises(IndexError):
                getattr(ex.MinHeap(), f)()
        rows = [([7], [7], 0), ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 0), ([5, 4, 3, 2, 1], [1, 2, 4, 5, 3], 6), ([3, 3, 3], [3, 3, 3], 0),
                ([58, 25, 91, 12, 70, 47, 84, 31, 63], [12, 25, 47, 31, 70, 91, 84, 58, 63], None)]
        for items, arr, swaps in rows:
            h = ex.MinHeap(items)
            self.assertEqual(h.a, arr)
            if swaps is not None:
                self.assertEqual(len(h.trace), swaps)
            self.assertEqual([h.pop() for _ in items], sorted(items))
        self.assertEqual([ex.is_heap(a) for a in ([], [1], [1, 3, 2], [2, 1], [1, 1, 1])], [True, True, True, False, True])

    def test_against_heapq(self) -> None:
        rng = random.Random(1)
        h, ref = ex.MinHeap(), []
        for _ in range(5000):
            if ref and rng.random() < 0.5:
                self.assertEqual(h.pop(), heapq.heappop(ref))
            else:
                x = rng.randint(0, 1000)
                h.push(x)
                heapq.heappush(ref, x)
            self.assertTrue(ex.is_heap(h.a))

    def test_examples(self) -> None:
        h = ex.MinHeap([25, 47, 12, 63, 31, 58, 70])
        self.assertEqual(h.a, [12, 31, 25, 63, 47, 58, 70])
        h.trace.clear()
        h.push(9)
        self.assertEqual(h.a, [9, 12, 25, 31, 47, 58, 70, 63])
        self.assertEqual(h.pop(), 9)
        self.assertEqual(h.a, [12, 31, 25, 63, 47, 58, 70])
        h2 = ex.MinHeap()
        h2.a = [5, 9, 7, 12, 10, 8]
        h2.push(4)
        self.assertEqual(h2.a, [4, 9, 5, 12, 10, 8, 7])
        h3 = ex.MinHeap()
        h3.a = [5, 9, 7, 12, 10, 8]
        self.assertEqual((h3.pop(), h3.a), (5, [7, 9, 8, 12, 10]))
        h4, arrays = ex.MinHeap(), []
        for x in (58, 25, 91, 12, 70):
            before = len(h4.trace)
            h4.push(x)
            arrays.append((list(h4.a), len(h4.trace) - before))
        self.assertEqual(arrays, [([58], 0), ([25, 58], 1), ([25, 58, 91], 0), ([12, 25, 91, 58], 2),
                                  ([12, 25, 91, 58, 70], 0)])


if __name__ == "__main__":
    unittest.main()
