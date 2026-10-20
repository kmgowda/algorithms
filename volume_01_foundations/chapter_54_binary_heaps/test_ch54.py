import heapq
import random
import unittest

import ch54_examples as ex


class TestChapter54(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
