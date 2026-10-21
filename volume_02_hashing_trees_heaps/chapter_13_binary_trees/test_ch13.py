import math
import unittest

import ch13_examples as ex


class TestChapter42(unittest.TestCase):
    def test_every_case(self) -> None:
        T = ex.TreeNode
        self.assertEqual((ex.count(None), ex.height(None), ex.count(T(1)), ex.height(T(1))), (0, -1, 1, 0))
        r = ex.from_array([58, 25, 84, 12, 47, 70, 91, 9])
        self.assertEqual((ex.count(r), ex.height(r), ex.from_array([])), (8, 3, None))
        chain = T(1, T(2, T(3)))
        self.assertEqual((ex.count(chain), ex.height(chain)), (3, 2))
        self.assertEqual((ex.children_of(0), ex.parent_of(0)), ((1, 2), -1))
        self.assertEqual((ex.evaluate(T(7)), ex.evaluate(T("-", T(5), T("+", T(2), T(1)))), ex.postfix(None)), (7, 2, []))
        with self.assertRaises(ZeroDivisionError):
            ex.evaluate(T("/", T(6), T(0)))

    def test_array_layout(self) -> None:
        for n in range(1, 200):
            root = ex.from_array(list(range(n)))
            self.assertEqual(ex.count(root), n)
            self.assertEqual(ex.height(root), int(math.log2(n)))
            for i in range(1, n):
                self.assertIn(i, ex.children_of(ex.parent_of(i)))
        self.assertEqual(ex.children_of(2), (5, 6))
        self.assertEqual(ex.parent_of(7), 3)

    def test_expressions(self) -> None:
        expr = ex.TreeNode("*", ex.TreeNode("+", ex.TreeNode(3), ex.TreeNode(4)), ex.TreeNode(2))
        self.assertEqual(ex.evaluate(expr), 14)
        self.assertEqual(ex.postfix(expr), [3, 4, "+", 2, "*"])
        e2 = ex.TreeNode("-", ex.TreeNode(5), ex.TreeNode("+", ex.TreeNode(2), ex.TreeNode(1)))
        self.assertEqual(ex.evaluate(e2), 2)
        self.assertEqual(2 ** 6 - 1, ex.count(ex.from_array(list(range(63)))))


if __name__ == "__main__":
    unittest.main()
