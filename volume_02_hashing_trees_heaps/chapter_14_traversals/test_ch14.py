import unittest

import ch14_examples as ex


class TestChapter43(unittest.TestCase):
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
