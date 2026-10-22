import collections
import random
import unittest

import ch09_examples as ex


class TestChapter27(unittest.TestCase):
    def test_every_case(self) -> None:
        r = ex.RingBuffer(3)
        with self.assertRaises(IndexError):
            r.dequeue()
        for x in "ABC":
            r.enqueue(x)
        with self.assertRaises(OverflowError):
            r.enqueue("D")
        self.assertEqual((r.front, r.back, r.count), (0, 0, 3))
        self.assertEqual((r.dequeue(), r.front), ("A", 1))
        r.enqueue("D")
        self.assertEqual((r.slots, r.items()), (["D", "B", "C"], ["B", "C", "D"]))
        one = ex.RingBuffer(1)
        one.enqueue(1)
        self.assertEqual((one.dequeue(), one.front, one.back), (1, 0, 0))
        v = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual((ex.window_max(v, 1), ex.window_max(v, 8), ex.window_max(v, 9), ex.window_max([], 3)),
                         (v, [9], [], []))
        self.assertEqual((ex.window_max([5, 5, 5], 2), ex.window_max([1, 2, 3, 4], 2), ex.window_max([4, 3, 2, 1], 2)),
                         ([5, 5], [2, 3, 4], [4, 3, 2]))

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

    def test_growing_and_one_empty(self) -> None:
        g = ex.GrowingRing(8)
        g.front = g.back = 3
        names = ["Ana", "Ben", "Cai", "Dev", "Eva", "Fay", "Gus", "Hal"]
        for n in names:
            g.enqueue(n)
        self.assertEqual(g.slots, ["Fay", "Gus", "Hal", "Ana", "Ben", "Cai", "Dev", "Eva"])
        g.enqueue("Ivy")
        self.assertEqual((len(g.slots), g.front, g.back, g.items()), (16, 0, 9, names + ["Ivy"]))
        z = ex.GrowingRing(0)
        z.enqueue(1)
        z.enqueue(2)
        self.assertEqual((z.items(), len(z.slots)), ([1, 2], 2))
        o = ex.OneEmptyRing(4)
        self.assertTrue(o.is_empty())
        with self.assertRaises(IndexError):
            o.dequeue()
        for x in "ABC":
            o.enqueue(x)
        self.assertTrue(o.is_full())
        with self.assertRaises(OverflowError):
            o.enqueue("D")                        # 4 seats hold only 3
        self.assertEqual((o.dequeue(), o.size()), ("A", 2))
        o.enqueue("D")
        self.assertEqual((o.slots, o.front, o.back, o.is_full()), ([None, "B", "C", "D"], 1, 0, True))
        self.assertEqual([o.dequeue() for _ in range(3)], ["B", "C", "D"])
        one = ex.OneEmptyRing(1)
        self.assertTrue(one.is_empty() and one.is_full())
        rng = random.Random(3)
        for cap in (1, 2, 3, 5):
            g, o, ref = ex.GrowingRing(cap), ex.OneEmptyRing(cap + 1), collections.deque()
            for _ in range(600):
                if rng.random() < 0.45 and ref:
                    want = ref.popleft()
                    self.assertEqual((g.dequeue(), o.dequeue()), (want, want))
                elif len(ref) < cap:
                    v = rng.randint(0, 99)
                    g.enqueue(v)
                    o.enqueue(v)
                    ref.append(v)
                else:
                    v = rng.randint(0, 99)
                    g.enqueue(v)                  # the growing ring never refuses
                    with self.assertRaises(OverflowError):
                        o.enqueue(v)
                    ref.append(v)
                    o = ex.OneEmptyRing(len(ref) + 1)
                    for w in ref:
                        o.enqueue(w)
                    cap = len(ref)
                self.assertEqual(g.items(), list(ref))
                self.assertEqual(o.size(), len(ref))

    def test_window_max(self) -> None:
        self.assertEqual(ex.window_max([3, 1, 4, 1, 5, 9, 2, 6], 3), [4, 4, 5, 9, 9, 9])
        rng = random.Random(2)
        for _ in range(500):
            xs = [rng.randint(0, 20) for _ in range(rng.randint(1, 15))]
            k = rng.randint(1, len(xs))
            self.assertEqual(ex.window_max(xs, k), [max(xs[i:i + k]) for i in range(len(xs) - k + 1)])


if __name__ == "__main__":
    unittest.main()
