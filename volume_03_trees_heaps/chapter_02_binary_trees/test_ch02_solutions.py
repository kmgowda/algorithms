import itertools
import math
import unittest

import ch02_examples as ex
import ch02_solutions as sol

T = ex.TreeNode


def all_shapes(n):
    """Every binary tree shape with n nodes (Catalan many)."""
    if n == 0:
        yield None
        return
    for k in range(n):
        for left, right in itertools.product(list(all_shapes(k)), list(all_shapes(n - 1 - k))):
            yield T(0, left, right)


def complete_by_definition(root) -> bool:
    """Level order with gaps written as None: complete exactly when no node comes after a gap."""
    order, seen_gap = [root], False
    for n in order:
        if n is None:
            seen_gap = True
            continue
        if seen_gap:
            return False
        order += [n.left, n.right]
    return True


class TestChapter02Solutions(unittest.TestCase):
    def test_small(self) -> None:
        self.assertTrue(sol.is_complete(None))
        self.assertEqual((sol.array_cells(None), sol.leaves(None)), (0, 0))
        self.assertTrue(sol.is_complete(T(1)))
        self.assertTrue(sol.is_complete(T(1, T(2))))
        self.assertFalse(sol.is_complete(T(1, None, T(2))))       # a right child with no left sibling

    def test_examples(self) -> None:
        self.assertTrue(sol.is_complete(ex.from_array([58, 25, 84, 12, 47, 70, 91, 9])))
        gap = T(50, T(30), T(70, None, T(80)))                     # Practice Problem 2
        self.assertEqual((sol.is_complete(gap), sol.array_cells(gap)), (False, 7))
        chain = T(1, None, T(2, None, T(3, None, T(4))))            # Thinking Problem 3
        self.assertEqual(sol.array_cells(chain), 15)
        long_chain = T(0)
        node = long_chain
        for v in range(1, 1000):
            node.right = T(v)
            node = node.right
        self.assertFalse(sol.is_complete(long_chain))               # stops early, no 1000-bit index needed
        self.assertEqual(sol.array_cells(long_chain), 2 ** 1000 - 1)

    def test_every_shape(self) -> None:
        for n in range(0, 8):
            for t in all_shapes(n):
                self.assertEqual(sol.is_complete(t), complete_by_definition(t))
                self.assertEqual(sol.is_complete(t), sol.array_cells(t) == n)
                self.assertLessEqual(sol.leaves(t), math.ceil(n / 2))         # Thinking Problem 1
                if sol.is_complete(t):
                    self.assertEqual(sol.leaves(t), math.ceil(n / 2))


if __name__ == "__main__":
    unittest.main()
