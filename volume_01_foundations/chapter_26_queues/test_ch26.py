import collections
import random
import unittest

import ch26_examples as ex


class TestChapter26(unittest.TestCase):
    def test_queue_against_deque(self) -> None:
        rng = random.Random(1)
        q, ref = ex.Queue(), collections.deque()
        for _ in range(3000):
            if ref and rng.random() < 0.45:
                self.assertEqual(q.dequeue(), ref.popleft())
            else:
                v = rng.randint(0, 99)
                q.enqueue(v)
                ref.append(v)
            self.assertEqual(q.is_empty(), not ref)
        with self.assertRaises(IndexError):
            ex.Queue().dequeue()

    def test_round_robin(self) -> None:
        self.assertEqual(ex.round_robin({"Ana": 3, "Ben": 1, "Cai": 2}),
                         [(1, "Ana", False), (2, "Ben", True), (3, "Cai", False), (4, "Ana", False),
                          (5, "Cai", True), (6, "Ana", True)])
        finished = {s: t for t, s, done in ex.round_robin({"Ana": 2, "Ben": 2, "Cai": 1}) if done}
        self.assertEqual(finished, {"Cai": 3, "Ana": 4, "Ben": 5})


if __name__ == "__main__":
    unittest.main()
