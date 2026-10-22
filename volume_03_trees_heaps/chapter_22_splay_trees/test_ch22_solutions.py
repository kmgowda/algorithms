import random
import unittest

import ch22_examples as ex
import ch22_solutions as sol


class TestChapter22Solutions(unittest.TestCase):
    def test_path_height(self) -> None:
        self.assertEqual([sol.path_splay_height(n) for n in range(1, 13)], [0, 1, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7])
        for n in range(3, 80):
            self.assertEqual(sol.path_splay_height(n), n // 2 + 1)

    def test_delete_range(self) -> None:
        t, gone = sol.delete_range(ex.SplayTree(), 1, 5)               # empty tree
        self.assertEqual((t.keys(), gone), ([], 0))
        t, gone = sol.delete_range(ex.SplayTree([7]), 7, 7)            # the only key
        self.assertEqual((t.keys(), gone), ([], 1))
        t, gone = sol.delete_range(ex.SplayTree([7]), 8, 9)            # nothing in range
        self.assertEqual((t.keys(), gone), ([7], 0))
        t, gone = sol.delete_range(ex.SplayTree(ex.SHELF), 30, 65)
        self.assertEqual((t.keys(), gone), ([12, 25, 70, 84, 91], 4))
        t, gone = sol.delete_range(ex.SplayTree(ex.SHELF), 65, 30)     # backwards range
        self.assertEqual(gone, 0)
        rng = random.Random(5)
        for _ in range(200):
            keys = rng.sample(range(100), rng.randrange(0, 30))
            a, b = sorted(rng.sample(range(-5, 105), 2))
            t, gone = sol.delete_range(ex.SplayTree(keys), a, b)
            self.assertTrue(t.valid())
            self.assertEqual(t.keys(), sorted(k for k in keys if not a <= k <= b))
            self.assertEqual(gone, sum(a <= k <= b for k in keys))

    def test_move_to_root_is_slow(self) -> None:
        self.assertEqual(sol.sequential_after_path(sol.MoveToRootTree, 5), 14)
        self.assertEqual(sol.sequential_after_path(sol.MoveToRootTree, 1000, 2), 1000998)
        self.assertEqual(sol.sequential_after_path(ex.SplayTree, 1000, 2), 8748)
        self.assertEqual(sol.sequential_after_path(sol.MoveToRootTree, 1), 0)


if __name__ == "__main__":
    unittest.main()
