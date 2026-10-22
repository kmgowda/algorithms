import random
import unittest

import ch09_solutions as sol
from ch09_examples import BTree


class TestChapter9Solutions(unittest.TestCase):
    def test_sorted_inserts_leave_minimum_nodes(self) -> None:
        self.assertEqual(sol.off_spine_sizes(BTree(3)), set())                 # empty tree: only the root
        self.assertEqual(sol.off_spine_sizes(BTree(3, [1, 2, 3])), set())      # one full root, no split yet
        for max_keys in (3, 5, 7, 9):
            for n in (max_keys + 1, 50, 333):
                self.assertEqual(sol.off_spine_sizes(BTree(max_keys, range(1, n + 1))), {max_keys // 2})

    def test_range_keys(self) -> None:
        self.assertEqual(sol.range_keys(BTree(3), 1, 9), ([], 1))              # empty tree
        self.assertEqual(sol.range_keys(BTree(3, [5]), 5, 5), ([5], 1))        # the only key
        self.assertEqual(sol.range_keys(BTree(3, [5]), 6, 9), ([], 1))
        t = BTree(3, [58, 25, 84, 12, 47, 70, 91, 31, 63])
        self.assertEqual(sol.range_keys(t, 30, 65), ([31, 47, 58, 63], 3))
        self.assertEqual(sol.range_keys(t, 65, 30), ([], 0))                   # backwards range
        rng = random.Random(8)
        for _ in range(300):
            mk = rng.choice((3, 5, 9))
            keys = rng.sample(range(500), rng.randint(0, 200))
            t = BTree(mk, keys)
            a, b = sorted(rng.sample(range(-10, 510), 2))
            got, reads = sol.range_keys(t, a, b)
            want = sorted(k for k in keys if a <= k <= b)
            self.assertEqual(got, want)
            self.assertLessEqual(reads, 2 * (t.height() + 1) + len(want) / (mk // 2))


if __name__ == "__main__":
    unittest.main()
