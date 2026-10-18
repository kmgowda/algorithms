import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestBTree(unittest.TestCase):
    def test_random_inserts(self) -> None:
        rng = random.Random(1)
        for t in (2, 3, 5):
            tree, model = ex.BTree(t), set()
            for _ in range(1500):
                k = rng.randint(0, 3000)
                tree.insert(k)
                model.add(k)
                if rng.random() < 0.05:
                    ex.check(tree)
            ex.check(tree)
            self.assertEqual(tree.keys_in_order(), sorted(model))
            for q in range(0, 3000, 37):
                self.assertEqual(tree.search(q), q in model)
            self.assertLessEqual(tree.height(), sol.max_height(len(model), t))

    def test_sorted_and_reads(self) -> None:
        tree = ex.BTree(3)
        for k in range(1, 101):
            tree.insert(k)
        ex.check(tree)
        tree.node_reads = 0
        tree.search(77)
        self.assertEqual(tree.node_reads, tree.height() + 1 if 77 not in tree.root.keys else 1)
        with self.assertRaises(ValueError):
            ex.BTree(1)

    def test_bplus_range(self) -> None:
        keys = list(range(0, 200, 5))
        chain = ex.BPlusLeafChain(keys)
        got, visited = chain.range(42, 80)
        self.assertEqual(got, [k for k in keys if 42 <= k <= 80])
        self.assertLessEqual(visited, 3)
        self.assertEqual(chain.range(500, 600)[0], [])

    def test_billion(self) -> None:
        self.assertLessEqual(ex.reads_for_billion(500), 4)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.max_keys(2, 2), 63)
        tree = ex.BTree(2)
        for k in [10, 20, 5, 6, 12, 30, 7, 17]:
            tree.insert(k)
        ex.check(tree)
        self.assertEqual(sol.minimum_key(tree), 5)
        self.assertGreaterEqual(sol.count_nodes(tree), 3)
        self.assertEqual(sol.max_height(1, 3), 0)


if __name__ == "__main__":
    unittest.main()
