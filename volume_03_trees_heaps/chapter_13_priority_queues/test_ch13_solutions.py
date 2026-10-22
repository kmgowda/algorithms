import random
import unittest

import ch13_solutions as sol


class TestChapter13Solutions(unittest.TestCase):
    def test_ageing_needs_no_rekeying(self) -> None:
        self.assertEqual(sol.aged_key(300, 0), sol.aged_key(50, 25))          # Challenge 1's tie at minute 25
        rng = random.Random(3)
        for _ in range(200):
            jobs = [(f"j{i}", rng.randint(1, 300), rng.randint(0, 40)) for i in range(rng.randint(0, 8))]
            fixed = [n for n, p, a in sorted(jobs, key=lambda j: (sol.aged_key(j[1], j[2]), j[2]))]
            for now in (40, 41, 90):
                self.assertEqual(sol.aged_order(jobs, now), fixed)

    def test_bucket_queue(self) -> None:
        q = sol.BucketPQ(1)                                                   # one level
        with self.assertRaises(IndexError):
            q.extract_min()
        q.insert(1, "only")
        self.assertEqual((len(q), q.extract_min(), len(q)), (1, (1, "only"), 0))
        q = sol.BucketPQ(3)
        for name, p in (("Ana", 3), ("Ben", 1), ("Cai", 2), ("Dev", 3)):
            q.insert(p, name)
        self.assertEqual([q.extract_min()[1] for _ in range(4)], ["Ben", "Cai", "Ana", "Dev"])
        rng = random.Random(1)
        q, ref, t = sol.BucketPQ(5), [], 0
        for _ in range(500):
            if ref and rng.random() < 0.4:
                ref.sort()
                p, _, item = ref.pop(0)
                self.assertEqual(q.extract_min(), (p, item))
            else:
                p = rng.randint(1, 5)
                q.insert(p, t)
                ref.append((p, t, t))
                t += 1

    def test_key_only_heap_is_unfair(self) -> None:
        self.assertEqual(sol.key_only_heap_order([]), [])
        self.assertEqual(sol.key_only_heap_order([(3, "a"), (3, "b")]), ["a", "b"])
        self.assertEqual(sol.key_only_heap_order([(3, "a"), (3, "b"), (3, "c")]), ["a", "c", "b"])
        self.assertEqual(sol.key_only_heap_order([(3, x) for x in "abcd"]), ["a", "d", "c", "b"])
        self.assertEqual(sol.key_only_heap_order([(5, "x"), (1, "y"), (9, "z")]), ["y", "x", "z"])


if __name__ == "__main__":
    unittest.main()
