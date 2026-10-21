import itertools
import random
import unittest

import ch29_examples as ex


class TestChapter29(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.tree_sum(list(range(1, 17))), ex.tree_sum(list(range(1, 1025)))[1:]), ((136, 15, 4), (1023, 10)))
        self.assertEqual(ex.prefix_sums_parallel([3, 1, 4, 1, 5, 9, 2, 6]), ([3, 4, 8, 9, 14, 23, 25, 31], 17, 3))
        self.assertEqual([round(ex.time_with_helpers(1023, 10, p), 1) for p in (1, 4, 32, 1024)], [1033.0, 265.8, 42.0, 11.0])
        self.assertEqual([round(ex.amdahl(0.9, p), 2) for p in (2, 8, 64, 1000)], [1.82, 4.71, 8.77, 9.91])

    def test_every_case(self) -> None:
        self.assertEqual((ex.tree_sum([]), ex.tree_sum([7]), ex.tree_sum([1, 2, 3])), ((0, 0, 0), (7, 0, 0), (6, 2, 2)))
        self.assertEqual((ex.prefix_sums_parallel([]), ex.prefix_sums_parallel([5])), (([], 0, 0), ([5], 0, 0)))
        self.assertEqual((ex.amdahl(1.0, 8), ex.amdahl(0.0, 8)), (8.0, 1.0))
        r = random.Random(29)
        for _ in range(200):
            v = [r.randint(-9, 9) for _ in range(r.randint(1, 40))]
            total, work, rounds = ex.tree_sum(v)
            self.assertEqual((total, work), (sum(v), len(v) - 1))
            self.assertEqual(ex.prefix_sums_parallel(v)[0], list(itertools.accumulate(v)))


if __name__ == "__main__":
    unittest.main()
