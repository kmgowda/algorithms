import sys
import unittest

import ch03_examples as ex


class TestChapter43(unittest.TestCase):
    def test_every_case(self) -> None:
        T = ex.TreeNode
        fns = (ex.preorder, ex.inorder, ex.postorder, ex.level_order, ex.inorder_iterative)
        self.assertEqual([f(None) for f in fns], [[]] * 5)
        self.assertEqual([f(T(5)) for f in fns], [[5]] * 5)
        left = T(3, T(2, T(1)))
        self.assertEqual([f(left) for f in fns[:4]], [[3, 2, 1], [1, 2, 3], [1, 2, 3], [3, 2, 1]])
        right = T(1, None, T(2, None, T(3)))
        self.assertEqual([f(right) for f in fns[:4]], [[1, 2, 3], [1, 2, 3], [3, 2, 1], [1, 2, 3]])
        full = ex.from_array([58, 25, 84, 12, 47, 70, 91])
        self.assertEqual(ex.postorder(full), [12, 47, 25, 70, 91, 84, 58])
        root = None
        for v in range(5000):
            root = T(v, root)
        old = sys.getrecursionlimit()
        sys.setrecursionlimit(1000)
        try:
            with self.assertRaises(RecursionError):
                ex.inorder(root)
        finally:
            sys.setrecursionlimit(old)
        self.assertEqual(len(ex.inorder_iterative(root)), 5000)
        self.assertEqual((ex.levels(None), ex.levels(T(5)), ex.levels(left)), ([], [[5]], [[3], [2], [1]]))
        self.assertEqual(ex.levels(ex.from_array([50, 30, 70, 20, 40, 60, 80, 10])),
                         [[50], [30, 70], [20, 40, 60, 80], [10]])
        self.assertEqual([row[-1] for row in ex.levels(ex.from_array([50, 30, 70, 20, 40, 60, 80, 10]))],
                         [50, 70, 80, 10])                                      # Practice Problem 2
        self.assertEqual(sum(ex.levels(full), []), ex.level_order(full))
        self.assertEqual(ex.folder_totals({"r": 0, "a": 3, "b": 4}, {"r": ["a", "b"]}, "r")["r"], 7)

    def test_orders(self) -> None:
        t = ex.from_array([58, 25, 84, 12, 47, 70, 91])
        self.assertEqual(ex.preorder(t), [58, 25, 12, 47, 84, 70, 91])
        self.assertEqual(ex.inorder(t), [12, 25, 47, 58, 70, 84, 91])
        self.assertEqual(ex.postorder(t), [12, 47, 25, 70, 91, 84, 58])
        self.assertEqual(ex.level_order(t), [58, 25, 84, 12, 47, 70, 91])
        for n in range(0, 40):
            tt = ex.from_array(list(range(n)))
            self.assertEqual(ex.inorder_iterative(tt), ex.inorder(tt))
            self.assertEqual(ex.level_order(tt), list(range(n)))
        small = ex.TreeNode(7, ex.TreeNode(3, ex.TreeNode(1), ex.TreeNode(5)), ex.TreeNode(9))
        self.assertEqual([ex.preorder(small), ex.inorder(small), ex.postorder(small), ex.level_order(small)],
                         [[7, 3, 1, 5, 9], [1, 3, 5, 7, 9], [1, 5, 3, 9, 7], [7, 3, 9, 1, 5]])
        totals = ex.folder_totals({"Home": 1, "Docs": 3, "Photos": 10, "Old": 2},
                                  {"Home": ["Docs", "Photos"], "Docs": ["Old"]}, "Home")
        self.assertEqual(totals, {"Old": 2, "Docs": 5, "Photos": 10, "Home": 16})


if __name__ == "__main__":
    unittest.main()
