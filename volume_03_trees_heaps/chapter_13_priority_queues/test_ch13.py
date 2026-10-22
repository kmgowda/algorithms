import random
import unittest

import ch13_examples as ex


class TestChapter53(unittest.TestCase):
    def test_every_case(self) -> None:
        for cls, err, ties in ((ex.UnsortedPQ, ValueError, list("adcb")), (ex.SortedPQ, IndexError, list("abcd")),
                               (ex.FairHeapPQ, IndexError, list("abcd"))):
            with self.assertRaises(err):
                cls().extract_min()
            q = cls()
            for it in "abcd":
                q.insert(1, it)
            self.assertEqual([q.extract_min()[1] for _ in range(4)], ties)
            q = cls()
            for p in (5, -2, 9, 0):
                q.insert(p)
            self.assertEqual([q.extract_min()[0] for _ in range(4)], [-2, 0, 5, 9])
        self.assertEqual([ex.shortest_first(j) for j in ([], [4], [3, 1, 2], [2, 2, 1])], [[], [4], [1, 2, 3], [1, 2, 2]])
        self.assertEqual((ex.finish_times([1, 2, 3]), ex.finish_times([3, 1, 2]), ex.finish_times([1, 2, 2])),
                         ([1, 3, 6], [3, 4, 6], [1, 3, 5]))

    def test_all_agree(self) -> None:
        rng = random.Random(1)
        for cls in (ex.UnsortedPQ, ex.SortedPQ, ex.FairHeapPQ):
            q, ref = cls(), []
            for _ in range(500):
                if ref and rng.random() < 0.4:
                    self.assertEqual(q.extract_min()[0], min(ref))
                    ref.remove(min(ref))
                else:
                    p = rng.randint(0, 50)
                    q.insert(p)
                    ref.append(p)

    def test_examples(self) -> None:
        pq = ex.FairHeapPQ()
        for name, pri in (("Ana", 3), ("Ben", 1), ("Cai", 2), ("Dev", 3)):
            pq.insert(pri, name)
        self.assertEqual([pq.extract_min()[1] for _ in range(4)], ["Ben", "Cai", "Ana", "Dev"])
        jobs = [300, 1, 12, 2, 45]
        self.assertEqual(sum(ex.finish_times(jobs)) / 5, 317.8)
        self.assertEqual(sum(ex.finish_times(ex.shortest_first(jobs))) / 5, 87.8)
        self.assertAlmostEqual(sum(ex.finish_times(ex.shortest_first([4, 1, 3]))) / 3, 13 / 3)


if __name__ == "__main__":
    unittest.main()
