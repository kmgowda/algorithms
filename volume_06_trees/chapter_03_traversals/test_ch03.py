import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def random_tree(rng, n, start=0):
    if n == 0:
        return None
    left = rng.randint(0, n - 1)
    return ex.Node(start + left, random_tree(rng, left, start), random_tree(rng, n - 1 - left, start + left + 1))


class TestTraversals(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = ex.Node("F", ex.Node("B", ex.Node("A"), ex.Node("D", ex.Node("C"), ex.Node("E"))),
                            ex.Node("G", None, ex.Node("I", ex.Node("H"))))

    def test_classic_orders(self) -> None:
        self.assertEqual(ex.preorder(self.tree), list("FBADCEGIH"))
        self.assertEqual(ex.inorder(self.tree), list("ABCDEFGHI"))
        self.assertEqual(ex.postorder(self.tree), list("ACEDBHIGF"))
        self.assertEqual(ex.level_order(self.tree), [["F"], ["B", "G"], ["A", "D", "I"], ["C", "E", "H"]])

    def test_iterative_match_recursive(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            t = random_tree(rng, rng.randint(0, 25))
            self.assertEqual(ex.inorder_iterative(t), ex.inorder(t))
            self.assertEqual(ex.preorder_iterative(t), ex.preorder(t))
            self.assertEqual(sol.postorder_iterative(t), ex.postorder(t))
            self.assertEqual(ex.inorder(t), sorted(ex.inorder(t)))      # random_tree builds search-tree order

    def test_expression_and_toc(self) -> None:
        expr = ex.Node("*", ex.Node("+", ex.Node(2), ex.Node(3)), ex.Node(4))
        self.assertEqual(ex.evaluate(expr), 20.0)
        self.assertEqual(ex.postorder(expr), [2, 3, "+", 4, "*"])
        book = ex.Node("Guide", ex.Node("Mammals", ex.Node("Lions")), ex.Node("Birds"))
        self.assertEqual(ex.table_of_contents(book), ["Guide", "  Mammals", "    Lions", "  Birds"])
        self.assertEqual(ex.level_order(None), [])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        t = ex.Node(3, ex.Node(9), ex.Node(20, ex.Node(15), ex.Node(7)))
        self.assertEqual(sol.zigzag_levels(t), [[3], [20, 9], [15, 7]])
        self.assertEqual(sol.right_side_view(t), [3, 20, 7])
        self.assertEqual(sol.level_averages(t), [3.0, 14.5, 11.0])
        self.assertEqual(sol.right_side_view(None), [])


if __name__ == "__main__":
    unittest.main()
