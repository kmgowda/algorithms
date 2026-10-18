import itertools
import math
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def inorder(node):
    out, stack = [], []
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.key)
        node = node.right
    return out


class TestDegenerate(unittest.TestCase):
    def test_heights(self) -> None:
        r = ex.height_report(500)
        self.assertEqual(r["sorted order"], 499)
        self.assertEqual(r["reverse order"], 499)
        self.assertLess(r["random order"], 40)
        self.assertEqual(r["best possible"], 8)

    def test_search_and_depth(self) -> None:
        stick = ex.build(list(range(1, 101)))
        self.assertEqual(ex.search_steps(stick, 100), 100)
        self.assertAlmostEqual(ex.average_depth(stick), 49.5)
        self.assertEqual(ex.average_depth(None), 0.0)

    def test_rebuild(self) -> None:
        rng = random.Random(1)
        for n in (1, 2, 7, 100, 1000):
            keys = list(range(n))
            rng.shuffle(keys)
            t = ex.rebuild_balanced(ex.build(keys))
            self.assertEqual(inorder(t), sorted(keys))
            self.assertEqual(ex.height(t), math.floor(math.log2(n)))

    def test_user_ids(self) -> None:
        self.assertEqual(ex.user_id_index(300), (299, 300))


class TestSolutions(unittest.TestCase):
    def test_stick_orders(self) -> None:
        for n in range(1, 7):
            count = sum(1 for p in itertools.permutations(range(n)) if ex.height(ex.build(list(p))) == n - 1)
            self.assertEqual(sol.stick_orders(n), count)

    def test_others(self) -> None:
        self.assertLess(sol.average_random_height(500, 10), 30)
        self.assertEqual(ex.height(ex.build(sol.zigzag_order(50))), 49)
        self.assertGreater(sol.max_steps_ratio(10**6), 40000)


if __name__ == "__main__":
    unittest.main()
