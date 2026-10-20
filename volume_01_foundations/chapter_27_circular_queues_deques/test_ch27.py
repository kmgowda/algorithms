import collections
import random
import unittest

import ch27_examples as ex


class TestChapter27(unittest.TestCase):
    def test_ring(self) -> None:
        rng = random.Random(1)
        ring, ref = ex.RingBuffer(5), collections.deque()
        for _ in range(3000):
            if rng.random() < 0.5 and ref:
                self.assertEqual(ring.dequeue(), ref.popleft())
            elif len(ref) < 5:
                v = rng.randint(0, 99)
                ring.enqueue(v)
                ref.append(v)
            else:
                with self.assertRaises(OverflowError):
                    ring.enqueue(0)
            self.assertEqual(ring.items(), list(ref))

    def test_window_max(self) -> None:
        self.assertEqual(ex.window_max([3, 1, 4, 1, 5, 9, 2, 6], 3), [4, 4, 5, 9, 9, 9])
        rng = random.Random(2)
        for _ in range(500):
            xs = [rng.randint(0, 20) for _ in range(rng.randint(1, 15))]
            k = rng.randint(1, len(xs))
            self.assertEqual(ex.window_max(xs, k), [max(xs[i:i + k]) for i in range(len(xs) - k + 1)])


if __name__ == "__main__":
    unittest.main()
