import math
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestAVL(unittest.TestCase):
    def test_random_operations_keep_invariants(self) -> None:
        rng = random.Random(1)
        root, model = None, set()
        for _ in range(4000):
            k = rng.randint(0, 300)
            if rng.random() < 0.6:
                root = ex.insert(root, k)
                model.add(k)
            else:
                root = ex.delete(root, k)
                model.discard(k)
            ex.check(root)
        self.assertEqual(list(ex.inorder(root)), sorted(model))
        for k in range(0, 301, 7):
            self.assertEqual(ex.contains(root, k), k in model)

    def test_sorted_input_stays_short(self) -> None:
        for n in (10, 100, 1000, 5000):
            root = None
            for k in range(n):
                root = ex.insert(root, k)
            self.assertLessEqual(ex.h(root), 1.45 * math.log2(n + 2))

    def test_example(self) -> None:
        root = None
        for k in [10, 20, 30, 40, 50, 25]:
            root = ex.insert(root, k)
        self.assertEqual(root.key, 30)
        self.assertEqual(list(ex.inorder(root)), [10, 20, 25, 30, 40, 50])
        h, first = ex.appointments_index(list(range(900, 1900)))
        self.assertLessEqual(h, 14)
        self.assertEqual(first, [900, 901, 902, 903, 904])

    def test_rotations_preserve_order(self) -> None:
        a, b, c = ex.Node("A"), ex.Node("B"), ex.Node("C")
        x, y = ex.Node("x"), ex.Node("y")
        y.left, y.right, x.left, x.right = x, c, a, b
        for n in (a, b, c):
            ex.update(n)
        ex.update(x)
        ex.update(y)
        top = ex.rotate_right(y)
        self.assertEqual(list(ex.inorder(top)), ["A", "x", "B", "y", "C"])
        self.assertEqual(list(ex.inorder(ex.rotate_left(top))), ["A", "x", "B", "y", "C"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.rotations_used([1, 2, 3]), 1)
        self.assertEqual(sol.rotations_used([3, 1, 2]), 2)
        self.assertEqual([sol.min_nodes_for_height(x) for x in range(6)], [1, 2, 4, 7, 12, 20])
        self.assertEqual(sol.max_avl_height(1000), 13)   # N(13) = 986 <= 1000 < N(14) = 1596
        self.assertLessEqual(sol.build_from_keys(list(range(1000))), 12)


if __name__ == "__main__":
    unittest.main()
